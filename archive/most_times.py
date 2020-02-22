import sys

# ===================================================
# Using instructor method
nums = sys.argv
max_count = 0
max_num = 0

start_list = 2
for num in nums[1:]:
    number_count = 1

    for second in nums[start_list:]:
        if num == second:
            number_count += 1

    if max_count < number_count:
        max_count = number_count
        max_num = num
    start_list += 1

print(max_num)

# ===================================================
# Sort each number
# then count as we loop over the sorted list
print("Using sorted list and loop:")
nums = sys.argv[1:]
nums = [ int(n) for n in nums]
nums.sort()

previous_num = nums[0]
current_count = 0
max_count = 0
max_num = 0

for num in nums:
    if num == previous_num:
        current_count += 1

        if current_count > max_count:
            max_count = current_count
            max_num = num
    else:
        previous_num = num
        current_count = 1

print("Number with most occurrence:", str(max_num))
print()

# =====================================================
# Using dictionaries
print("Using dictionaries:")
nums_dict = {}
input = sys.argv[1:]

# store number in nums dict
for n in input:
    nums_dict[n] = nums_dict.get(n, 0) + 1

# find number with most occurence
max_count = 0
max_num = 0

for key in nums_dict:
    if(nums_dict[key] > max_count):
        max_count = nums_dict[key]
        max_num = key

print("Number with most occurrence:", str(max_num))