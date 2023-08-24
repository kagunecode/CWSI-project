from drone_features.draw_gui import GUI
from drone_features.connection import connect

def main():
    drone = connect()
    gui = GUI(drone)
    gui.run()

if __name__ == "__main__":
    main()
