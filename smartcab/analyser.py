import matplotlib.pyplot as plt
f = file('test_q_100_final.txt')
contents = f.read().split('\n')
count_trials = 100
neg_rewards_count = dict()
for i in range(0, len(contents)):
    if 'Environment.reset()' in contents[i]:
        i = i + 1
        while i < len(contents) and ('Environment.step()' not in contents[i] and 'Environment.act()' not in contents[i]):
            neg_rewards_count[100 - count_trials] = neg_rewards_count.get(100 - count_trials, 0) + 1
            i = i + 1
        count_trials = count_trials - 1
values = []
for i in range(0, 100):
    values.append(neg_rewards_count.get(i, 0))

plt.plot(range(0, 100), values, label='Q Learning Agent', color='g', marker=',')

f = file('test_random.txt')
contents = f.read().split('\n')
count_trials = 100
neg_rewards_count_rand = dict()
for i in range(0, len(contents)):
    if 'Environment.reset()' in contents[i]:
        i = i + 1
        while i < len(contents) and ('Environment.step()' not in contents[i] and 'Environment.act()' not in contents[i]):
            neg_rewards_count_rand[100 - count_trials] = neg_rewards_count_rand.get(100 - count_trials, 0) + 1
            i = i + 1
        count_trials = count_trials - 1
values2 = []
for i in range(0, 100):
    values2.append(neg_rewards_count_rand.get(i, 0))
plt.plot(range(0, 100), values2, label='Random Learning Agent', color='r', marker='.')

plt.title('Negative Rewards in each trial')
plt.xlabel('Number of Trials')
plt.ylabel('Frequency of Negative Rewards')
plt.legend()
plt.show()