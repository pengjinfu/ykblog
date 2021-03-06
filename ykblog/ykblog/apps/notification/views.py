
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *



class notificationView(APIView):
    '''返回一个用户通知'''
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):

        user = request.user

        try:
            notification = Notification.objects.get(pk=pk)
        except Notification.DoesNotExist as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if user!=notification.user_id:

                return Response(status=status.HTTP_403_FORBIDDEN)


            data = NotificationSerializer(notification,many=True)

            return Response({"data":data.data},status=status.HTTP_200_OK)


class UserNotificationView(APIView):
    """
    获取用户的新通知
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        real_user = request.user

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if user!=real_user:

                return Response(status=status.HTTP_403_FORBIDDEN)
            # 只返回上次看到的通知以来发生的新通知
            # 比如用户在 10:00:00 请求一次该API，在 10:00:10 再次请求该API只会返回 10:00:00 之后产生的新通知
            since = request.query_params.get('since', 0.0)

            notifications = Notification.objects.select_related('user').filter(user=user).filter(
                timestamp__gt=since).order_by("timestamp")

            data = NotificationSerializer(notifications,many=True)

            return Response({"data": data.data}, status=status.HTTP_200_OK)