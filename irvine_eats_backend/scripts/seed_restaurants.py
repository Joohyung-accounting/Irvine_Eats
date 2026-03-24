import argparse
from irvine_eats_backend.app import routes


def main():
    parser = argparse.ArgumentParser(
        description="Seed Irvine Eats restaurants from Google Places."
    )
    parser.add_argument(
        "--location",
        default=routes.LOCATION,
        help="lat,lng (default: routes.LOCATION)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=routes.RADIUS,
        help="meters (default: routes.RADIUS)",
    )
    args = parser.parse_args()

    count = routes.upsert_restaurants_from_places(
        location=args.location,
        radius=args.radius,
    )
    print(f"Done: {count} restaurants upserted into {routes.DB_PATH}")


if __name__ == "__main__":
    main()