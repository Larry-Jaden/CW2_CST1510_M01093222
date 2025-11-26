import pandas as pd
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents, get_incidents_by_severity
from app.data.datasets import get_all_datasets
from app.data.tickets import get_all_tickets
from app.data.users import get_all_users

def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)
    
    # 1. Setup database
    print("\n[1/5] Setting up database...")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    print("✅ Database setup complete")
    
    # 2. Migrate users
    print("\n[2/5] Migrating users...")
    user_count = migrate_users_from_file()
    print(f"✅ Migrated {user_count} users")
    
    # 3. Test authentication
    print("\n[3/5] Testing authentication...")
    success, msg = register_user("demo_user", "DemoPass123!", "analyst")
    print(f"   Register: {msg}")
    
    success, msg = login_user("demo_user", "DemoPass123!")
    print(f"   Login: {msg}")
    
    # 4. Test CRUD operations
    print("\n[4/5] Testing CRUD operations...")
    conn = connect_database()
    
    # Create incident
    incident_id = insert_incident(
        "2024-11-05",
        "Demo Incident",
        "High",
        "Open",
        "This is a demo incident for testing"
    )
    print(f"   Created incident #{incident_id}")
    
    # Read incidents
    df_incidents = get_all_incidents()
    print(f"   Total incidents: {len(df_incidents)}")
    
    # Read datasets
    df_datasets = get_all_datasets()
    print(f"   Total datasets: {len(df_datasets)}")
    
    # Read tickets
    df_tickets = get_all_tickets()
    print(f"   Total tickets: {len(df_tickets)}")
    
    conn.close()
    
    # 5. Display summary
    print("\n[5/5] Database Summary:")
    print("-" * 40)
    
    users = get_all_users()
    print(f"Users: {len(users)}")
    
    df_incidents = get_all_incidents()
    print(f"Incidents: {len(df_incidents)}")
    
    df_datasets = get_all_datasets()
    print(f"Datasets: {len(df_datasets)}")
    
    df_tickets = get_all_tickets()
    print(f"Tickets: {len(df_tickets)}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()