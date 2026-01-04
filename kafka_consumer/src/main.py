from infrastructure.factories.manager_factory import ManagerFactory
import time

def main():
    ManagerFactory.create_all()
    
    # Keep the consumer running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Consumer shutting down...")

if __name__ == "__main__":
    main()
