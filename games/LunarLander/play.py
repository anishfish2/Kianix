
import gym
from stable_baselines3 import DQN



env = gym.make('LunarLander-v2', render_mode="human")  # continuous: LunarLanderContinuous-v2
env.reset()

model = DQN('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10000)

episodes = 10

for ep in range(episodes):
	env.render()
	done = False
	while not done:
		action, _states = model.predict(obs)
		obs, reward, done, info, idk = env.step(action)
		env.render()

env.close()