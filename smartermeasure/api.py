import requests
from smartermeasure import (USERS_QUERY_PARAMS, USERS_ENDPOINT, SIGNON_ENDPOINT,
                            REPORTLINK_ENDPOINT, RESULTS_QUERY_PARAMS, RESULTS_ENDPOINT)
from smartermeasure.errors import QueryStringError, MissingUserIdError


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
        return result.status_code


class SmarterMeasure(object):

    def __init__(self, access_key, secret):
        self.client = Client(access_key, secret)

    class Users(object):
        def __init__(self, client, user_id=None):
            self.client = client
            self.user_id = user_id

        def get(self):
            if not self.user_id:
                raise MissingUserIdError()
            r = self.client('GET', USERS_ENDPOINT + '/' + self.user_id)
            return r.json()

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
            return r.json()

        def sign_on(self, ssl=True, include_settings=False, redirect_to_section=None):
            if not self.user_id:
                raise MissingUserIdError()
            data = {'UseSSL': ssl, 'IncludeSettings': include_settings}
            if redirect_to_section:
                data['RedirectToSection'] = redirect_to_section
            r = self.client('POST', SIGNON_ENDPOINT.format(user_id=self.user_id), data=data)
            return r.json()

        def report_link(self):
            if not self.user_id:
                raise MissingUserIdError()
            r = self.client('GET', REPORTLINK_ENDPOINT.format(self.user_id))
            return r.json()

    def user(self, user_id):
        """Gets a User by Id

        :param user_id: The user id
        :type user_id: str
        :return: User details
        :rtype: dict
        """
        return self.Users(self.client, user_id=user_id).get()

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