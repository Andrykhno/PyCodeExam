# Accommodation Booking App

class Accommodation:
    def __init__(self, id, name, location, price, availability=True):
        self.id = id
        self.name = name
        self.location = location
        self.price = price
        self.availability = availability

    def __str__(self):
        status = "Available" if self.availability else "Booked"
        return f"{self.id}. {self.name} in {self.location} - ${self.price}/night [{status}]"


class BookingSystem:
    def __init__(self):
        self.accommodations = []
        self.bookings = {}

    def add_accommodation(self, id, name, location, price):
        accommodation = Accommodation(id, name, location, price)
        self.accommodations.append(accommodation)

    def view_accommodations(self):
        print("\nAvailable Accommodations:")
        for acc in self.accommodations:
            print(acc)

    def book_accommodation(self, id, customer_name):
        for acc in self.accommodations:
            if acc.id == id:
                if acc.availability:
                    acc.availability = False
                    self.bookings[id] = customer_name
                    print(f"\nBooking confirmed for {acc.name} by {customer_name}.")
                else:
                    print("\nThis accommodation is already booked.")
                return
        print("\nAccommodation ID not found!")

    def view_bookings(self):
        print("\nCurrent Bookings:")
        if not self.bookings:
            print("No bookings made yet.")
        else:
            for id, customer in self.bookings.items():
                print(f"{self.accommodations[id - 1].name}: Booked by {customer}")


def main():
    system = BookingSystem()

    # Adding sample accommodations
    system.add_accommodation(1, "Sea View Apartment", "Miami", 120)
    system.add_accommodation(2, "Mountain Cabin", "Aspen", 150)
    system.add_accommodation(3, "City Center Hotel", "New York", 200)

    while True:
        print("\n--- Accommodation Booking System ---")
        print("1. View Accommodations")
        print("2. Book Accommodation")
        print("3. View Bookings")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            system.view_accommodations()
        elif choice == "2":
            try:
                acc_id = int(input("Enter Accommodation ID to book: "))
                customer_name = input("Enter your name: ")
                system.book_accommodation(acc_id, customer_name)
            except ValueError:
                print("Invalid input. Please enter numeric IDs.")
        elif choice == "3":
            system.view_bookings()
        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()