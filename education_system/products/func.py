from products.models import Group, Product, Enrollment
from users.models import User

from django.utils import timezone


def add_user_group(product: Product, user: User):
    groups = product.groups.all()

    if not groups.exists():
        group = Group.objects.create(product=product, name_group=f'Group_1')
        Enrollment.objects.create(group=group, student=user)
    else:
        group = min(groups, key=lambda group_len: group_len.students.count())

        if group.students.count() >= product.max_group_len:
            group = Group.objects.create(product=product, name_group=f'Group_{groups.count() + 1}')

        Enrollment.objects.create(group=group, student=user)


def redistribute_groups(product: Product):
    if product.start_data > timezone.now():
        groups = list(product.groups.all())
        students = [student for group in groups for student in group.students.all()]

        optimal_size = max(min(len(students) // len(groups), product.max_group_len), product.min_group_len)

        for group in groups:
            group.students.clear()

        for ind, student in enumerate(students):
            if ind < (optimal_size * len(groups)):
                group = groups[ind // optimal_size]
            else:
                if groups[ind % optimal_size].students.count() >= product.max_group_len:
                    group = Group.objects.create(name_group=f'Group_{len(groups) + 1}', product=product)
                    groups.append(group)
                else:
                    group = groups[ind % optimal_size]
            Enrollment.objects.create(group=group, student=student)
