from stable_baselines3 import PPO
from env.execution_env import ExecutionEnv
from config import MarketParams

params = MarketParams()
env = ExecutionEnv(params)

model = PPO("MlpPolicy", env, verbose=1, n_steps=2048, batch_size=64)
model.learn(total_timesteps=500_000)
model.save("models/ppo_baseline")


