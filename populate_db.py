"""
Script to populate machine database
Currently creates:
10 Machines on Sittner Floor 1
1 Machine on Foreman Floor 2
2 Machines on each floor for Foreman Floor 3-7
3 Machines on Conard Floor 1
1 Machine on each floor for Conard Floors 2-4
"""
import requests
#pylint: disable=W3101
def create_machine(public_id,floor,floor_id,dorm):
    """
    Function to call Post machine endpoints
    Parameters: Counter for public_id, floor number, floor_id, and dorm
    Returns: Nothing
    """
    requests.post(
        f"http://localhost:5000/machine/{public_id}",
        params={
            "floor_id": floor_id,
            "floor":floor,
            "dorm": dorm,
            "status": "free",
            "last_service_date": "01-10-01",
            "installation_date": "01-10-2001",
        },
        )
def main():
    """
    Runs loops to create machines for each dorm.
    """
    counter=1
    #Create Machines for Sittner
    for i in range(1,11):
        create_machine(counter,1,i,"Sittner")
        counter+=1
    create_machine(counter,2,1,"Foreman")
    counter+=1
    #Create Machines for Foreman
    for i in range(3,8):
        for j in range(1,3):
            create_machine(counter,i,j,"Foreman")
            counter+=1
    #Create Machines for Conard floor 1
    for i in range(1,4):
        create_machine(counter,1,i,"Conard")
        counter+=1
    #Create Machines for the rest of Conard
    for i in range(2,5):
        create_machine(counter,i,1,"Conard")
        counter+=1

if __name__=="__main__":
    main()
