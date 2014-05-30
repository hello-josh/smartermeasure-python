from .api import SmarterMeasure
__all__ = ['SmarterMeasure', 'APICallError', 'QueryStringError']

USERS_ENDPOINT = 'https://api.smartermeasure.com/v3/users'
USERS_QUERY_PARAMS = {'UserId', 'InternalID', 'Email', 'FirstName', 'LastName', 'AccessCode', 'OrderBy',
                      'ExcludeCustomQuestions', 'limit', 'offset', 'AssessmentKey', 'AdministrativeGroupKey'}
RESULTS_ENDPOINT = 'https://api.smartermeasure.com/v3/results'
RESULTS_QUERY_PARAMS = {'UserID', 'InternalID', 'FirstName', 'LastName', 'EmailAddress', 'Gender',
                        'AdminGroupUserName', 'TestingGroupUserName', 'ExtendedData', 'IncludeAccountRequestedData',
                        'StartDate', 'EndDate', 'UpdateStartDate', 'UpdateEndDate', 'StartRecord', 'EndRecord'}

SIGNON_ENDPOINT = 'https://api.smartermeasure.com/v3/users/{user_id}/signon'
REPORTLINK_ENDPOINT = 'https://api.smartermeasure.com/v3/users/{user_id}/reportlink'