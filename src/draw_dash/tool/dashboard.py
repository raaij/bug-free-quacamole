from draw_dash.constant import PATH_DRAW_DASH

def read_dashboard_code():
    with open(PATH_DRAW_DASH / "frontend2" / "dashboard_screen.py") as file:
        code = file.read()

    return code

def modify_dashboard_code(content: str):
    with open(PATH_DRAW_DASH / "frontend2" / "dashboard_screen.py", "w") as file:
        file.write(content)

    return "Successfully wrote dashboard code"
