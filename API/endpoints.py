"""
OrangeHRM REST API v2 base path (demo site).

Why not `/api/employees`:
- That URL returns 404 on the public demo. Real routes live under
  `/web/index.php/api/v2/...` and require a Bearer token.

What you need for TestAPI/ tests:
- Set ORANGEHRM_API_TOKEN in Env/.env (OAuth token from your OrangeHRM instance).
- Without it, tests in TestAPI/ are skipped so Jenkins/UI runs stay green.
"""
BASE_API = "https://opensource-demo.orangehrmlive.com/web/index.php/api/v2"

GET_EMPLOYEES = "/pim/employees"
CREATE_EMPLOYEE = "/pim/employees"
DELETE_EMPLOYEE = "/pim/employees/"
DELETE_USER = "/admin/users/"
