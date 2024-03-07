from rest_framework import serializers, viewsets
from products.models import Lesson, Product, ProductValid, Group
from users.models import User


class ProductSerializer(serializers.ModelSerializer):
    lessons_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['author', 'name', 'start_data', 'price', 'lessons_cnt']

    def get_lessons_cnt(self, obj):
        return Lesson.objects.filter(product=obj).count()


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name_lesson', 'url_lesson']


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        products = ProductValid.objects.filter(user=self.request.user).values_list('product', flat=True)
        return Lesson.objects.filter(product__in=products)


class StatisticsSerializer(serializers.ModelSerializer):
    cnt_students = serializers.SerializerMethodField()
    avg_group = serializers.SerializerMethodField()
    avg_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'cnt_students', 'avg_group', 'avg_product']

    def get_cnt_students(self, obj):
        return ProductValid.objects.filter(product=obj).count()

    def get_avg_group(self, obj):
        groups = Group.objects.filter(product=obj)
        cnt_student = sum(group.students.count() for group in groups)
        max_cnt_student = obj.max_group_len * groups.count()
        if max_cnt_student == 0:
            return 0
        return (cnt_student / max_cnt_student) * 100

    def get_avg_product(self, obj):
        success_product = ProductValid.objects.filter(product=obj).count()
        all_student = User.objects.all()
        if all_student == 0:
            return 0
        return (success_product / all_student) * 100


class StatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StatisticsSerializer
    queryset = Product.objects.all()
