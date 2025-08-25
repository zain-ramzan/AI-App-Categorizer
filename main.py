import csv
import argparse
from data_sources import snap, flathub, apple_store, gog, itch_io, myabandonware
from utils.helpers import normalize_category # Assuming normalize_labels is still useful for tag processing
from category_processing.processor import (
    select_main_category,
    assign_energy_tag,
)
from config import STATIC_CATEGORIES # Import STATIC_CATEGORIES from config

def fetch_app_data(app_name):
    """Fetch application data (tags only) from all sources."""
    snap_cats = snap.get_categories(app_name)
    flat_cats = flathub.get_categories(app_name)
    apple_cats = apple_store.get_categories(app_name)
    gog_cats = gog.get_categories(app_name)
    itch_cats = itch_io.get_categories(app_name)
    abandon_cats = myabandonware.get_categories(app_name)

    # Organize all results in a dictionary (tags only)
    raw_categories = {
        "Snapcraft": snap_cats,
        "Flathub": flat_cats,
        "Apple Store": apple_cats,
        "Gog": gog_cats,
        "Itch.io": itch_cats,
        "My Abandonware": abandon_cats,
    }

    # Filter empty results
    non_empty_results = {k: v for k, v in raw_categories.items() if v}
    return non_empty_results

def process_app(app_name):
    """
    Process a single application, determine its category and energy label.
    """
    # Fetch data (tags only)
    non_empty_results = fetch_app_data(app_name)
    if not non_empty_results:
        return app_name, "No such app", "Unknown" # Return default for category and energy label

    # Select main category based on static matching and special rules
    # Pass STATIC_CATEGORIES to the select_main_category function
    main_cat = select_main_category(app_name, non_empty_results, list(STATIC_CATEGORIES))

    # Assign energy label based on the main category
    energy_label = assign_energy_tag(main_cat)

    return app_name, main_cat, energy_label

def batch_process(input_file, output_file):
    """
    Process applications from a file in batch mode.
    """
    try:
        with open(input_file, 'r') as infile:
            apps = [line.strip() for line in infile if line.strip()] # Read non-empty lines

        results = []
        for app_name in apps:
            app_name, main_cat, energy_label = process_app(app_name)
            results.append((app_name, main_cat, energy_label))

        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Application', 'Category', 'EnergyLabel'])
            writer.writerows(results)

        return output_file

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return None
    except Exception as e:
        print(f"An error occurred during batch processing: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Categorize desktop applications.")
    parser.add_argument(
        "app_name",
        nargs="?", # Make app_name optional
        help="Name of the application to categorize."
    )
    parser.add_argument(
        "-i", "--input",
        help="Input CSV file with a list of application names."
    )
    parser.add_argument(
        "-o", "--output",
        help="Output CSV file for batch processing results."
    )

    args = parser.parse_args()

    if args.app_name and (args.input or args.output):
        print("Error: Cannot specify both a single app name and input/output files.")
        exit(1)

    if args.input and not args.output:
        print("Error: Output file is required when specifying an input file.")
        exit(1)

    if args.app_name:
        # Process single application
        app_name, category, energy_label = process_app(args.app_name)
        print(f"Application: {app_name}")
        print(f"Category: {category}")
        print(f"Energy Label: {energy_label}")
    elif args.input and args.output:
        # Process batch from file
        print(f"Processing applications from {args.input}...")
        output_file = batch_process(args.input, args.output)
        if output_file:
            print(f"Batch processing complete. Results written to {output_file}")
    else:
        print("Please provide either an application name or specify input and output files for batch processing.")
        parser.print_help()
