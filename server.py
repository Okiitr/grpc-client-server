import grpc
from concurrent import futures
import user_management_pb2
import user_management_pb2_grpc

# In-memory database
users_db = {}

class UserManagementService(user_management_pb2_grpc.UserManagementServiceServicer):
    def CreateUser(self, request, context):
        user_id = len(users_db) + 1
        user = user_management_pb2.User(id=user_id, name=request.name, email=request.email)
        users_db[user_id] = user
        return user_management_pb2.CreateUserResponse(user=user)

    def GetUser(self, request, context):
        user = users_db.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_management_pb2.GetUserResponse()
        return user_management_pb2.GetUserResponse(user=user)

    def UpdateUser(self, request, context):
        user = users_db.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_management_pb2.UpdateUserResponse()
        user.name = request.name
        user.email = request.email
        users_db[request.id] = user
        return user_management_pb2.UpdateUserResponse(user=user)

    def DeleteUser(self, request, context):
        if request.id not in users_db:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_management_pb2.DeleteUserResponse(message="User not found")
        del users_db[request.id]
        return user_management_pb2.DeleteUserResponse(message="User deleted successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_management_pb2_grpc.add_UserManagementServiceServicer_to_server(UserManagementService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
