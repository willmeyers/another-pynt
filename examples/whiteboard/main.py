from app import App


def main():
    client = App()

    while client.running:
        client.run_app()

    client.close()


if __name__ == '__main__':
    main()