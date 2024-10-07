import grpc
import user_management_pb2
import user_management_pb2_grpc

def run():
    # Establish connection
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_management_pb2_grpc.UserManagementServiceStub(channel)

    # Create a new user
    print("Creating a new user")
    create_response = stub.CreateUser(user_management_pb2.CreateUserRequest(name="John Doe", email="john@example.com"))
    print(f"User created: {create_response.user}")

    # Retrieve the user
    print("\nRetrieving user")
    get_response = stub.GetUser(user_management_pb2.GetUserRequest(id=create_response.user.id))
    print(f"User retrieved: {get_response.user}")

    # Update the user
    print("\nUpdating user")
    update_response = stub.UpdateUser(user_management_pb2.UpdateUserRequest(id=create_response.user.id, name="John Updated", email="john_updated@example.com"))
    print(f"User updated: {update_response.user}")

    # Delete the user
    print("\nDeleting user")
    delete_response = stub.DeleteUser(user_management_pb2.DeleteUserRequest(id=create_response.user.id))
    print(f"Response: {delete_response.message}")

if __name__ == '__main__':
    run()
