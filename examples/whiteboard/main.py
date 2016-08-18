from app import App


def main():
    client = App()

    while client.running:
        client.run()

    client.close()


if __name__ == '__main__':
    main()