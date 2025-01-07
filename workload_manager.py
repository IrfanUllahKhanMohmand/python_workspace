import csv

def main():
    print("Academic Workload Manager\n")
    staff_name = input("Enter staff name: ")
    role = input("Enter role (e.g., Lecturer, Module Leader): ")
    contract_type = input("Enter contract type (Full-Time/Part-Time): ")

    # Initialize workload categories
    workload = {
        "ATSR": 0,
        "TS": 0,
        "TLR": 0,
        "SA": 0,
        "Other": 0
    }

    activities = []

    while True:
        print("\nAdd a new activity:")
        activity_type = input("Enter activity type (ATSR, TS, TLR, SA, Other): ")
        activity_description = input("Enter activity description: ")
        trimester = input("Enter trimester (Trimester 1, Trimester 2, Trimester 3, All Year): ")
        hours_per_instance = float(input("Enter hours per instance: "))
        instances = int(input("Enter number of instances: "))

        total_hours = hours_per_instance * instances
        workload[activity_type] += total_hours

        activities.append({
            "Type": activity_type,
            "Description": activity_description,
            "Trimester": trimester,
            "Hours": total_hours
        })

        add_more = input("Add another activity? (yes/no): ").strip().lower()
        if add_more != "yes":
            break

    # Calculate totals
    total_hours_allocated = sum(workload.values())
    
    # Display workload summary
    print("\nWorkload Summary for {}:\n".format(staff_name))
    print("Role: {}".format(role))
    print("Contract Type: {}\n".format(contract_type))

    print("Workload Allocation:")
    for category, hours in workload.items():
        print("  {}: {} hours".format(category, hours))

    print("\nTotal Hours Allocated: {} hours".format(total_hours_allocated))
    print("Maximum Allowable Hours: 1570 hours")
    if total_hours_allocated > 1570:
        print("WARNING: Workload exceeds maximum allowable hours!")
    else:
        print("Workload is within the allowable limit.")

    # Display activity breakdown
    print("\nActivity Breakdown:")
    for i, activity in enumerate(activities, 1):
        print("{}. Type: {}, Description: {}, Trimester: {}, Hours: {}".format(
            i, activity["Type"], activity["Description"], activity["Trimester"], activity["Hours"]
        ))

    # Option to export to CSV
    export = input("\nWould you like to export the workload summary to a CSV file? (yes/no): ").strip().lower()
    if export == "yes":
        export_to_csv(staff_name, role, contract_type, workload, activities)


def export_to_csv(staff_name, role, contract_type, workload, activities):
    filename = f"{staff_name.replace(' ', '_')}_workload_summary.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["Academic Workload Summary"])
        writer.writerow(["Staff Name", staff_name])
        writer.writerow(["Role", role])
        writer.writerow(["Contract Type", contract_type])
        writer.writerow([])

        # Write workload allocation
        writer.writerow(["Category", "Hours"])
        for category, hours in workload.items():
            writer.writerow([category, hours])
        writer.writerow([])

        # Write activity breakdown
        writer.writerow(["Activity Breakdown"])
        writer.writerow(["Type", "Description", "Trimester", "Hours"])
        for activity in activities:
            writer.writerow([activity["Type"], activity["Description"], activity["Trimester"], activity["Hours"]])

    print(f"\nWorkload summary exported to {filename}")


if __name__ == "__main__":
    main()
