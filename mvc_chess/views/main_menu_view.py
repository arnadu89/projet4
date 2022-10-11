class MainMenuView:
    @classmethod
    def main_menu_view(cls):
        print("-- MVC Chess --\n")
        print("1. List players")
        print("2. List tournaments")
        print("Q. Quit")
        return input("Choice : ")
