import core.solveRoom as sr
import core.resetRoom as rr
import core.fetchCSRF as fc
import time

while True:
    csrf_token = fc.get_csrf_token_simple()
    if csrf_token and rr.main(csrf_token):
        time.sleep(1)
        sr.main(csrf_token)
        break
    else:
        continue

input("\nPress ENTER to exit")
