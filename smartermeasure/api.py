from .errors import *
import requests

USERS_ENDPOINT = 'https://api.smartermeasure.com/v3/users'
USERS_QUERY_PARAMS = {'UserId', 'InternalID', 'Email', 'FirstName', 'LastName', 'AccessCode', 'OrderBy',
                      'ExcludeCustomQuestions', 'PageSize', 'Page', 'AssessmentKey', 'AdministrativeGroupKey'}
RESULTS_ENDPOINT = 'https://api.smartermeasure.com/v3/results'
RESULTS_QUERY_PARAMS = {'UserID', 'InternalID', 'FirstName', 'LastName', 'EmailAddress', 'Gender',
                        'AdminGroupUserName', 'TestingGroupUserName', 'ExtendedData', 'IncludeAccountRequestedData',
                        'StartDate', 'EndDate', 'UpdateStartDate', 'UpdateEndDate', 'StartRecord', 'EndRecord'}
SIGNON_ENDPOINT = 'https://api.smartermeasure.com/v3/users/{user_id}/signon'
REPORTLINK_ENDPOINT = 'https://api.smartermeasure.com/v3/users/{user_id}/reportlink'


class Client(object):
    def __init__(self, access_key, secret):
        self.access_key = access_key
        self.secret = secret

    def __call__(self, method, url, params=None, data=None, headers=None):
        r = requests.request(method=method, url=url, params=params, data=data, headers=headers,
                             auth=(self.access_key, self.secret))
        self._raise_on_status(r)
        return r

    @staticmethod
    def _raise_on_status(result):
        """Raises a named exception on API return code errors

        :param result: API response
        :type result: requests.Response
        """
        if result.status_code < 400:
            return
        data = result.json()
        ex = data.get("RestException", {})
        error_map = {
            "InvalidInput": InvalidInputError,
            "AuthenticationFailed": AuthenticationFailedError,
            "InternalError": InternalError,
            "InvalidAuthenticationInfo": InvalidAuthenticationInfoError,
            "InvalidProtocol": InvalidProtocolError,
            "InvalidUri": InvalidUriError,
            "ResourceNotFound": ResourceNotFoundError,
            "UnsupportedHttpVerb": UnsupportedHttpVerbError
        }
        cls = error_map.get(ex.get('Code'), APICallError)
        raise cls(ex.get('Status', 500), ex.get('ExtendedDetails', "Unknown Internal Error"))


class SmarterMeasure(object):

    def __init__(self, access_key, secret):
        self.client = Client(access_key, secret)

    class Users(object):
        def __init__(self, client, user_id=None):
            self.client = client
            self.user_id = user_id

        def __call__(self, *args, **kwargs):
            if len(**kwargs):
                return self.search(**kwargs)
            if len(args):
                # allow users(1) to return a new Users object with the new user_id
                return self.__class__(self.client, user_id=args[0])
            if not self.user_id:
                raise MissingUserIdError()
            r = self.client('GET', USERS_ENDPOINT + '/' + self.user_id)
            self._data = r.json()
            return self
        get = __call__

        def __getitem__(self, item):
            """Allows dict access to object for user's details"""
            return self.data.__getitem__(item)
        __getattr__ = __getitem__

        @property
        def data(self):
            if getattr(self, '_data'):
                return self._data
            return self()

        def search(self, **kwargs):
            """Searches for users

            Keyword Arguments:
                UserId                  Only show users with this UserID.
                InternalID              Only show users with this InternalID.
                Email                   Only show users with this email address.
                FirstName               Only show users with this first name.
                LastName                Only show users with this last name.
                AccessCode              Only show users with this access code.
                OrderBy                 How the results should be ordered.
                ExcludeCustomQuestions  If the return should exclude the custom questions. default True
                limit                   The number of records to limit the return to, the max limit is 1000. default 50
                offset                  The row that the results should start with, used for paging. default 1
                AssessmentKey           The Group Key that is assigned to the assessment to filter by. This can be a comma delimited list of keys to search within.
                AdministrativeGroupKey  The primary Administrative Group Key that is assigned to the assessment to filter by. This can be a comma delimited string of keys to search within.
            """
            # check unknown query string parameters
            unknowns = set(kwargs) - USERS_QUERY_PARAMS
            if unknowns:
                raise QueryStringError("Parameter(s) %s" % unknowns)

            r = self.client('GET', USERS_ENDPOINT, params=kwargs)
            result = r.json()
            if int(result['Total']):
                # map user `dict`s to `User` objects
                if isinstance(result['User'], list):
                    users = []
                    for u in result['User']:
                        new_user = self.__class__(self.client, u['UserId'])
                        new_user._data = u
                        users.append(new_user)
                    result['User'] = users
                else:
                    new_user = self.__class__(self.client, result['User']['UserId'])
                    new_user._data = result['User']
                    result['User'] = new_user
            return result

        def sign_on(self, ssl=True, include_settings=False, redirect_to_section=None):
            if not self.user_id:
                raise MissingUserIdError()
            data = {'UseSSL': ssl, 'IncludeSettings': include_settings}
            if redirect_to_section:
                data['RedirectToSection'] = redirect_to_section
            r = self.client('POST', SIGNON_ENDPOINT.format(user_id=self.user_id), data=data)
            response = r.json()
            return response['RedirectUrl']

        def report_link(self):
            if not self.user_id:
                raise MissingUserIdError()
            r = self.client('GET', REPORTLINK_ENDPOINT.format(user_id=self.user_id))
            response = r.json()
            return response['EntryLink']

    def user(self, user_id):
        """Gets a User by Id

        :param user_id: The user id
        :type user_id: str
        :return: The user
        :rtype: smartermeasure.api.SmarterMeasure.Users
        """
        return self.Users(self.client, user_id=user_id)

    def users(self, **kwargs):
        """Searches for users

        Keyword Arguments:
            UserId                  Only show users with this UserID.
            InternalID              Only show users with this InternalID.
            Email                   Only show users with this email address.
            FirstName               Only show users with this first name.
            LastName                Only show users with this last name.
            AccessCode              Only show users with this access code.
            OrderBy                 How the results should be ordered.
            ExcludeCustomQuestions  If the return should exclude the custom questions. default True
            limit                   The number of records to limit the return to, the max limit is 1000. default 50
            offset                  The row that the results should start with, used for paging. default 1
            AssessmentKey           The Group Key that is assigned to the assessment to filter by. This can be a comma delimited list of keys to search within.
            AdministrativeGroupKey  The primary Administrative Group Key that is assigned to the assessment to filter by. This can be a comma delimited string of keys to search within.
        """
        return self.Users(self.client).search(**kwargs)

    def register(self, first_name, last_name, email, group_key, gender=None, internal_id=None):
        """Registers a user with SmarterMeasure

        :param first_name: User's first name
        :type first_name: str
        :param last_name: The user's last name
        :type last_name: str
        :param email: The user's email
        :type email: str
        :param group_key: Key to match with the proper assessment
        :type group_key: str
        :param gender: M or F
        :type gender: str
        :param internal_id: Consumer's internal ID for the user
        :type internal_id: str
        :return: The new user object
        :rtype: Users
        """
        data = {'GroupKey': group_key, 'FirstName': first_name,
                'LastName': last_name, 'Email': email}
        if gender:
            data['Gender'] = gender
        if internal_id:
            data['InternalID'] = internal_id
        r = self.client('POST', USERS_ENDPOINT, data=data)
        return self.Users(self.client, user_id=r.json()['UserId'])

    def results(self, **kwargs):
        """Searches for assessment results
        
        Keyword Arguments:
            UserID                       This can be a comma sep. list of SmarterMeasure user Ids.
            InternalID                   InternalID
            FirstName                    FirstName
            LastName                     LastName
            EmailAddress                 EmailAddress
            Gender                       Gender
            AdminGroupUserName           AdminGroupUserName
            TestingGroupUserName         TestingGroupUserName
            ExtendedData                 If passed, the results will include the detailed scores for the sections passed in here. This is a comma delimited list. Valid data points are LifeFactors, LearnStyles, PersonalAttributes, TechComp, TechKnowledge, Demographic.
            IncludeAccountRequestedData  default  false
            StartDate                    When wanting to filter by date started, this is the start date of the date range.
            EndDate                      When wanting to filter by date started, this is the end date of the date range.
            UpdateStartDate              When wanting to filter by date updated, this is the start date of the date range.
            UpdateEndDate                When wanting to filter by date updated, this is the end date of the date range.
            StartRecord                  default 1
            EndRecord                    default 50
        """
        unknowns = set(kwargs) - RESULTS_QUERY_PARAMS
        if unknowns:
            raise QueryStringError("Parameter(s) %s" % unknowns)
        r = self.client('GET', RESULTS_ENDPOINT, params=kwargs)
        return r.json()