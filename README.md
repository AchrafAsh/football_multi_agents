## Notes

- Red: team 1
- Blue: team 2
- Set the frames per second max (it's very slow)

## Simulations

### Game 1 (new utility)

![](./new_utilities.png)

| Team | Possession | Passes |
|------|------------|--------|
| 1    | 123        | 70     |
| 2    | 217        | 82     | 

- Winner: **Team 2**

### Game 2 (new utility)

![](./new_utility_2.png)

| Team | Possession | Passes |
|------|------------|--------|
| 1    | 236        | 98     |
| 2    | 217        | 56     | 

- Winner: **Team 1**

### Game 3 (old/simple utility)

![](./old_utility_1.png)

| Team | Possession | Passes |
|------|------------|--------|
| 1    | 206        | 4      |
| 2    | 300        | 3      | 

- Winner: **Team 1**

### Game 4 (old/simple utility)

![](./old_utility_2.png)

| Team | Possession | Passes |
|------|------------|--------|
| 1    | 166        | 2      |
| 2    | 230        | 4      | 

- Winner: **Team 2**


## Resources:
- [Deepmind Article](https://www.deepmind.com/blog/advancing-sports-analytics-through-ai-research)
- [Kaggle Competition](https://www.kaggle.com/c/google-football)
- [Google Football Repo](https://github.com/google-research/football)

## Agents:
- team -> player / attacker + defender + goal-keeper
- ball

## TODO:
- Créer la class `Player` avec les [attributs](https://www.fifplay.com/encyclopedia/player-attributes/):
    - speed
    - dribbling (probability of keeping the ball)
    - defending (probability of taking to the ball)
    - intercepting (probability to intercept the ball)
    - shot (initial ball speed)
- Ajouter des agents `GoalKeeper`?
- Ajouter les `Reporters`