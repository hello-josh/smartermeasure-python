import requests

__all__ = ['SmarterMeasureClient', 'APICallError', 'QueryStringError']

USERS_ENDPOINT = 'https://api.smartermeasure.com/v3/users'
USERS_QUERY_PARAMS = {'UserId', 'InternalID', 'Email', 'FirstName', 'LastName', 'AccessCode', 'OrderBy',
                      'ExcludeCustomQuestions', 'limit', 'offset', 'AssessmentKey', 'AdministrativeGroupKey'}
RESULTS_ENDPOINT = 'https://api.smartermeasure.com/v3/results'
RESULTS_QUERY_PARAMS = {'UserID', 'InternalID', 'FirstName', 'LastName', 'EmailAddress', 'Gender',
                        'AdminGroupUserName', 'TestingGroupUserName', 'ExtendedData', 'IncludeAccountRequestedData',
                        'StartDate', 'EndDate', 'UpdateStartDate', 'UpdateEndDate', 'StartRecord', 'EndRecord'}

SIGNON_ENDPOINT = 'https://api.smartermeasure.com/v3/users/{user_id}/signon'
REPORTLINK_ENDPOINT = 'https://api.smartermeasure.com/v3/users/{user_id}/reportlink'


class SmarterMeasureClient(object):
    def __init__(self, access_key, secret):
        self.access_key = access_key
        self.secret = secret

    def users(self, *args, **kwargs):
        if len(args) == 1:
            return self._user_id(args[0])
        elif len(args) > 1:
            raise Exception("users() only takes a single positional arg: userid")
        # check unknown query string parameters
        unknowns = set(kwargs) - USERS_QUERY_PARAMS
        if unknowns:
            raise QueryStringError("Parameter(s) %s" % unknowns)

        r = self._call_sm('GET', USERS_ENDPOINT, params=kwargs)
        return r.json()

    def _user_id(self, user_id):
        r = self._call_sm('GET', USERS_ENDPOINT + '/' + user_id)
        return r.json()

    def sign_on(self, user_id, ssl=True, include_settings=False, redirect_to_section=None):
        data = {'UseSSL': ssl, 'IncludeSettings': include_settings}
        if redirect_to_section:
            data['RedirectToSection'] = redirect_to_section
        r = self._call_sm('POST', SIGNON_ENDPOINT.format(user_id=user_id), data=data)
        return r.json()

    def report_link(self, user_id):
        r = self._call_sm('GET', REPORTLINK_ENDPOINT.format(user_id))
        return r.json()

    def results(self, **kwargs):
        unknowns = set(kwargs) - RESULTS_QUERY_PARAMS
        if unknowns:
            raise QueryStringError("Parameter(s) %s" % unknowns)
        r = self._call_sm('GET', RESULTS_ENDPOINT, params=kwargs)
        return r.json()

    def _call_sm(self, method, url, params=None, data=None, headers=None):
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


class APICallError(Exception):
    pass


class QueryStringError(APICallError):
    pass