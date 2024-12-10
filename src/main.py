from files import cp_directory, generate_pages_recursive

def main():
    cp_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()