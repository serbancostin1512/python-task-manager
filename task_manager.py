
import json


FILE_NAME = "tasks.json"


def load_tasks():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def show_tasks(tasks):
    if not tasks:
        print("\nNu ai nicio sarcina.")
        return

    print("\n=== LISTA DE SARCINI ===")

    for index, task in enumerate(tasks, start=1):
        status = "Finalizata" if task["completed"] else "In lucru"
        print(f"{index}. {task['title']} - {status}")


def add_task(tasks):
    title = input("Introdu numele sarcinii: ").strip()

    if not title:
        print("Numele sarcinii nu poate fi gol.")
        return

    tasks.append({
        "title": title,
        "completed": False
    })

    save_tasks(tasks)
    print("Sarcina a fost adaugata!")


def complete_task(tasks):
    show_tasks(tasks)

    if not tasks:
        return

    try:
        number = int(input("Numarul sarcinii finalizate: "))

        if number < 1 or number > len(tasks):
            print("Numar invalid.")
            return

        tasks[number - 1]["completed"] = True
        save_tasks(tasks)
        print("Sarcina a fost finalizata!")

    except ValueError:
        print("Introdu un numar valid.")


def delete_task(tasks):
    show_tasks(tasks)

    if not tasks:
        return

    try:
        number = int(input("Numarul sarcinii de sters: "))

        if number < 1 or number > len(tasks):
            print("Numar invalid.")
            return

        removed_task = tasks.pop(number - 1)
        save_tasks(tasks)
        print(f"A fost stearsa sarcina: {removed_task['title']}")

    except ValueError:
        print("Introdu un numar valid.")


def main():
    tasks = load_tasks()

    while True:
        print("\n=== PYTHON TASK MANAGER ===")
        print("1. Afiseaza sarcinile")
        print("2. Adauga o sarcina")
        print("3. Finalizeaza o sarcina")
        print("4. Sterge o sarcina")
        print("0. Iesire")

        choice = input("Alege o optiune: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "0":
            print("La revedere!")
            break
        else:
            print("Optiune invalida. Incearca din nou.")


if __name__ == "__main__":
    main()
