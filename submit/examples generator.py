import numpy
import numpy as np
import math


# get total price and projects map with projects prices
# return list of lists each list contain list possible projects, their total cost,
# and variable that tell if there is a bigger group
def create_list_of_possible_projects(total, projects_map):
    return_list = []
    # move over the projects
    for first_project in range(len(projects_map)):
        # check if the project cost is less then the total price
        if projects_map[first_project] <= total:
            # if less add to the return list the project
            return_list.append([[first_project], projects_map[first_project], False])
            index_on_return_list = len(return_list) - 1
            # move over the project- check where can add current project
            for project in range(len(projects_map)):
                first_check_index = index_on_return_list  # start index
                last_check_index = len(return_list) - 1  # end index
                while first_check_index <= last_check_index:
                    if project not in return_list[first_check_index][0]:
                        # check if can add the current project
                        if return_list[first_check_index][1] + projects_map[project] <= total:
                            return_list[first_check_index][2] = True  # there is a bigger list
                            new_option = return_list[first_check_index][0].copy()  # copy the list
                            new_option.append(project)  # add the new project
                            new_option.sort()
                            # add the new list to the return list
                            return_list.append([new_option,
                                                return_list[first_check_index][1] + projects_map[project], False])
                    first_check_index += 1
    return return_list


# create list of lists, each list contain projects that their total cost not must be equal to the total price
def create_list_of_possible_projects_no_equal(total, projects_map):
    full_list = create_list_of_possible_projects(total, projects_map)
    remove_list = []
    for index in range(len(full_list)):
        if not full_list[index][2] and full_list[index][0] not in remove_list:
            remove_list.append(full_list[index][0])
    return remove_list

# get list and check if there is duplicate item
def has_duplicate(project_list_to_check):
    s = []
    for item in project_list_to_check:
        if item in s:
            return True
        s.append(item)
    return False


# with hidden duplicates
# def get_projects_first_assumption(benefits_matrix_):
#     # benefits of each project if chosen
#     most_satisfied_voters = 0
#     most_satisfied_voters_index = 0
#     # for each possible choice of projects
#     for chosen_projects_index in range(len(list_of_possible_projects)):
#         satisfied_voters_current_choice = 0
#         # for example - list_of_possible_projects[chosen_project_index]= [0,2]. project_index= 0 then 1
#         chosen_projects = list_of_possible_projects[chosen_projects_index]
#         for voter_row in benefits_matrix_:
#             # chosen_projects[project_index]= 0 then 2
#             for project_index in range(len(chosen_projects)):
#                 if (voter_row[chosen_projects[project_index]] == 1):
#                     satisfied_voters_current_choice += 1
#                     break
#
#         if satisfied_voters_current_choice > most_satisfied_voters:
#             most_satisfied_voters = satisfied_voters_current_choice
#             most_satisfied_voters_index = chosen_projects_index
#     return list_of_possible_projects[most_satisfied_voters_index]


def get_projects_first_assumption(benefits_matrix_):
    # benefits of each project if chosen
    most_satisfied_voters = 0
    list_of_maximizing_choices = []
    # for each possible choice of projects
    for chosen_projects_index in range(len(list_of_possible_projects)):
        satisfied_voters_current_choice = 0
        # for example - list_of_possible_projects[chosen_project_index]= [0,2]. project_index= 0 then 1
        chosen_projects = list_of_possible_projects[chosen_projects_index]
        for voter_row in benefits_matrix_:
            # chosen_projects[project_index]= 0 then 2
            for project_index in range(len(chosen_projects)):
                if (voter_row[chosen_projects[project_index]] == 1):
                    satisfied_voters_current_choice += 1
                    break

        if satisfied_voters_current_choice >= most_satisfied_voters:
            if satisfied_voters_current_choice > most_satisfied_voters:
                list_of_maximizing_choices.clear()
            most_satisfied_voters = satisfied_voters_current_choice
            most_satisfied_voters_index = chosen_projects_index
            list_of_maximizing_choices.append(list_of_possible_projects[most_satisfied_voters_index])
    return list_of_maximizing_choices


# with hidden duplicates
# def get_projects_second_assumption(benefits_matrix_):
#     # benefits of each project(sum of columns) if chosen
#     result = [sum(x) for x in zip(*benefits_matrix_)]
#     best_sum = 0
#     index_of_best_sum = 0
#     # for each possible choice of projects
#     for index in range(len(list_of_possible_projects)):
#         sum_of_current_index = 0
#         # sum the benefits of chosen projects
#         for j in range(len(list_of_possible_projects[index])):
#             sum_of_current_index += result[list_of_possible_projects[index][j]]
#         if sum_of_current_index > best_sum:
#             best_sum = sum_of_current_index
#             index_of_best_sum = index
#     return list_of_possible_projects[index_of_best_sum]

def get_projects_second_assumption(benefits_matrix_):
    # benefits of each project(sum of columns) if chosen
    result = [sum(x) for x in zip(*benefits_matrix_)]
    best_sum = 0
    index_of_best_sum = 0
    list_of_maximizing_choices = []
    # for each possible choice of projects
    for index in range(len(list_of_possible_projects)):
        sum_of_current_index = 0
        # sum the benefits of chosen projects
        for j in range(len(list_of_possible_projects[index])):
            sum_of_current_index += result[list_of_possible_projects[index][j]]
        if sum_of_current_index >= best_sum:
            if sum_of_current_index > best_sum:
                list_of_maximizing_choices.clear()
            best_sum = sum_of_current_index
            index_of_best_sum = index
            list_of_maximizing_choices.append(list_of_possible_projects[index_of_best_sum])
    return list_of_maximizing_choices


#   with hidden duplicates
# def get_projects_third_assumption(benefits_matrix_):
#     # benefits of each project(sum of columns) if chosen
#     voters_count_for_each_project = [sum(x) for x in zip(*benefits_matrix_)]
#     best_sum = 0
#     index_of_best_sum = 0
#     # for each possible choice of projects
#     for chosen_project_index in range(len(list_of_possible_projects)):
#         utilities_sum_current_choice = 0
#         # sum the benefits of chosen projects
#         # for example - list_of_possible_projects[chosen_project_index]= [0,2]. project_index= 0 then 1
#         chosen_projects = list_of_possible_projects[chosen_project_index]
#         for project in chosen_projects:
#             # utility- sum for each chosen project: num of voters for the project * cost of the project.
#             utilities_sum_current_choice += voters_count_for_each_project[project] * projects_price[project]
#         if utilities_sum_current_choice > best_sum:
#             best_sum = utilities_sum_current_choice
#             index_of_best_sum = chosen_project_index
#     return list_of_possible_projects[index_of_best_sum]

def get_projects_third_assumption(benefits_matrix_):
    # benefits of each project(sum of columns) if chosen
    voters_count_for_each_project = [sum(x) for x in zip(*benefits_matrix_)]
    best_sum = 0
    index_of_best_sum = 0
    list_of_maximizing_choices = []
    # for each possible choice of projects
    for chosen_project_index in range(len(list_of_possible_projects)):
        utilities_sum_current_choice = 0
        # sum the benefits of chosen projects
        # for example - list_of_possible_projects[chosen_project_index]= [0,2]. project_index= 0 then 1
        chosen_projects = list_of_possible_projects[chosen_project_index]
        for project in chosen_projects:
            # utility- sum for each chosen project: num of voters for the project * cost of the project.
            utilities_sum_current_choice += voters_count_for_each_project[project] * projects_price[project]
        if utilities_sum_current_choice >= best_sum:
            if utilities_sum_current_choice > best_sum:
                list_of_maximizing_choices.clear()
            best_sum = utilities_sum_current_choice
            index_of_best_sum = chosen_project_index
            list_of_maximizing_choices.append(list_of_possible_projects[index_of_best_sum])
    return list_of_maximizing_choices


#   with hidden duplicates
# def get_projects_fourth_assumption(benefits_matrix_):
#     # benefits of each project(sum of columns) if chosen
#     voters_count_for_each_project = [sum(x) for x in zip(*benefits_matrix_)]
#     best_sum = 0
#     index_of_best_sum = 0
#     # for each possible choice of projects
#     for chosen_project_index in range(len(list_of_possible_projects)):
#         utilities_sum_current_choice = 0
#         # sum the benefits of chosen projects
#         # for example - list_of_possible_projects[chosen_project_index]= [0,2]. project_index= 0 then 1
#         chosen_projects = list_of_possible_projects[chosen_project_index]
#         for project in chosen_projects:
#             # utility- sum for each chosen project: num of voters for the project * cost of the project.
#             utilities_sum_current_choice += voters_count_for_each_project[project] * math.sqrt(projects_price[project])
#         if utilities_sum_current_choice > best_sum:
#             best_sum = utilities_sum_current_choice
#             index_of_best_sum = chosen_project_index
#     return list_of_possible_projects[index_of_best_sum]

def get_projects_fourth_assumption(benefits_matrix_):
    # benefits of each project(sum of columns) if chosen
    voters_count_for_each_project = [sum(x) for x in zip(*benefits_matrix_)]
    best_sum = 0
    index_of_best_sum = 0
    list_of_maximizing_choices = []
    # for each possible choice of projects
    for chosen_project_index in range(len(list_of_possible_projects)):
        utilities_sum_current_choice = 0
        # sum the benefits of chosen projects
        # for example - list_of_possible_projects[chosen_project_index]= [0,2]. project_index= 0 then 1
        chosen_projects = list_of_possible_projects[chosen_project_index]
        for project in chosen_projects:
            # utility- sum for each chosen project: num of voters for the project * cost of the project.
            utilities_sum_current_choice += voters_count_for_each_project[project] * math.sqrt(projects_price[project])
        if utilities_sum_current_choice >= best_sum:
            if utilities_sum_current_choice > best_sum:
                list_of_maximizing_choices.clear()
            best_sum = utilities_sum_current_choice
            index_of_best_sum = chosen_project_index
            list_of_maximizing_choices.append(list_of_possible_projects[index_of_best_sum])
    return list_of_maximizing_choices


# with hidden duplicates
# def get_projects_fifth_assumption(benefits_matrix_):
#     best_sum = 0
#     index_of_best_sum = 0
#
#     for chosen_project_index in range(len(list_of_possible_projects)):
#         chosen_projects = list_of_possible_projects[chosen_project_index]
#         #create a list whose len is number of projects(num of columns in matrix)
#         chosen_projects_padded=numpy.asarray([0]*benefits_matrix_.shape[1])
#         for chosen_project in chosen_projects:
#             chosen_projects_padded[chosen_project]=1
#
#         utilities_sum_current_choice=0
#         for voter_row in benefits_matrix_:
#             M1=voter_row
#             M2=chosen_projects_padded
#             M3=projects_price_list
#             #cost of the most pricey project from chosen projects for this voter
#             current_voter_best_from_choosen = np.max(M1 *M2 *M3, axis=0)
#             #the utility is the sum of cost of the most pricey project from chosen projects for each voter
#             utilities_sum_current_choice+=current_voter_best_from_choosen
#
#         if utilities_sum_current_choice > best_sum:
#             best_sum = utilities_sum_current_choice
#             index_of_best_sum = chosen_project_index
#
#     return list_of_possible_projects[index_of_best_sum]


def get_projects_fifth_assumption(benefits_matrix_):
    best_sum = 0
    index_of_best_sum = 0
    list_of_maximizing_choices = []

    for chosen_project_index in range(len(list_of_possible_projects)):
        chosen_projects = list_of_possible_projects[chosen_project_index]
        # create a list whose len is number of projects(num of columns in matrix)
        chosen_projects_padded = numpy.asarray([0] * benefits_matrix_.shape[1])
        for chosen_project in chosen_projects:
            chosen_projects_padded[chosen_project] = 1

        utilities_sum_current_choice = 0
        for voter_row in benefits_matrix_:
            M1 = voter_row
            M2 = chosen_projects_padded
            M3 = projects_price_list
            # cost of the most pricey project from chosen projects for this voter
            current_voter_best_from_choosen = np.max(M1 * M2 * M3, axis=0)
            # the utility is the sum of cost of the most pricey project from chosen projects for each voter
            utilities_sum_current_choice += current_voter_best_from_choosen

        if utilities_sum_current_choice >= best_sum:
            if utilities_sum_current_choice > best_sum:
                list_of_maximizing_choices.clear()
            best_sum = utilities_sum_current_choice
            index_of_best_sum = chosen_project_index
            list_of_maximizing_choices.append(list_of_possible_projects[index_of_best_sum])

    return list_of_maximizing_choices


projects_num_list = {3, 4, 5, 6, 7, 8, 9}
total_price = 50
k_acc_to_projects_num = {3: [2, 3], 4: [2, 3], 5: [2, 3, 4], 6: [2, 3, 4, 5], 7: [2, 3, 4, 5], 8: [2, 3, 4, 5],
                         9: [2, 3, 4, 5, 6]}
voters_acc_to_projects_num = {3: [2, 3, 4], 4: [2, 3, 4, 5, 6], 5: [2, 3, 4, 5, 6], 6: [3, 4, 5, 6], 7: [3, 4, 5, 6],
                              8: [3, 4, 5, 6], 9: [3, 4, 5]}

number_of_examples = 0
whole_program_run_count = 0
# stop after there is 5 good examples
while number_of_examples < 500:
    # print(whole_program_run_count)
    whole_program_run_count += 1
    for projects_num in projects_num_list:
        for voters_num in voters_acc_to_projects_num[projects_num]:
            for k in k_acc_to_projects_num[projects_num]:
                projects_price_list = numpy.random.choice(numpy.arange(1, total_price + 1), projects_num, replace=False)
                projects_price = dict(zip(range(len(projects_price_list)), projects_price_list))

                # for start- create the list of projects list
                list_of_possible_projects = create_list_of_possible_projects_no_equal(total_price, projects_price)

                # print(whole_program_run_count, projects_num, voters_num, k)

                for iteration in range(20):
                    # create benefits matrix
                    benefits_matrix = numpy.empty(shape=(voters_num, projects_num), dtype=int)
                    for v_row in range(voters_num):
                        benefits_matrix[v_row] = np.array([1] * k + [0] * (projects_num - k))
                        np.random.shuffle(benefits_matrix[v_row])
                    list_assumptions = []
                    final_1st_assumption = get_projects_first_assumption(benefits_matrix)  # first assumption
                    final_2nd_assumption = get_projects_second_assumption(benefits_matrix)  # second assumption
                    list_assumptions.extend(final_1st_assumption)
                    list_assumptions.extend(final_2nd_assumption)
                    # improve runtime
                    if has_duplicate(list_assumptions):
                        continue
                    final_3rd_assumption = get_projects_third_assumption(benefits_matrix)  # third assumption
                    final_4th_assumption = get_projects_fourth_assumption(benefits_matrix)  # fourth assumption
                    final_5th_assumption = get_projects_fifth_assumption(benefits_matrix)  # fifth assumption
                    list_assumptions.extend(final_3rd_assumption)
                    list_assumptions.extend(final_4th_assumption)
                    list_assumptions.extend(final_5th_assumption)

                    # check that there is no duplicate assumptions
                    if not has_duplicate(list_assumptions):
                        number_of_examples += 1  # good example
                        # print all
                        print(benefits_matrix)
                        print(list(projects_price.values()))
                        print("First Assumption:", final_1st_assumption)
                        print("second assumption:", final_2nd_assumption)
                        print("third assumption:", final_3rd_assumption)
                        print("fourth assumption:", final_4th_assumption)
                        print("fifth assumption:", final_5th_assumption)
                        print("/////////////////////////////////////////////")
