import sys


def main():
    try:
        from price_tracker.price_tracker import main
        args = sys.argv[1:]
        main(args)
    except KeyboardInterrupt:
        print('')
        sys.exit(0)


if __name__ == '__main__':
    main()
