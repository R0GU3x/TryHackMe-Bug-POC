import core.solveRoom as sr
import core.resetRoom as rr
import core.fetchCSRF as fc
import time

csrf_token = fc.get_csrf_token_simple()

if rr.main(csrf_token):
    time.sleep(2)
    sr.main(csrf_token)

input("Press ENTER to exit")
