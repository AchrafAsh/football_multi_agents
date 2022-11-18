## Resources:
- [Deepmind Article](https://www.deepmind.com/blog/advancing-sports-analytics-through-ai-research)
- [Kaggle Competition](https://www.kaggle.com/c/google-football)
- [Google Football Repo](https://github.com/google-research/football)

## Agents:
- team -> player / attacker + defender + goal-keeper
- ball

## Attributes:
- have the ball
- defender / attacker (based on who has the ball)
- speed
- dribbling skills (influence the probability P of losing the ball)

## Actions:
- move towards the goal / closer attacker (attacker / defender)
- shoot if close to the goal
- take the ball with probability P if close to the ball owner
- call for proposal and passing the ball
- intercepting the ball if in the trajectory of a pass

## TODO:
- Créer l'environement (quadrillage du terrain, les cages de foot)
- Créer la class `Ball` (sous classe d'un agent)
- Créer la class `Player` avec les [attributs](https://www.fifplay.com/encyclopedia/player-attributes/):
    - speed
    - dribbling (probability of keeping the ball)
    - defending (probability of taking to the ball)
    - intercepting (probability to intercept the ball)
    - shot (initial ball speed)
- Créer les `Reporters`

## Optional:
- use an RL model for movement
    - reward = ball possession + goals
    - use heuristic first

- use Turtle for the environment [](https://www.youtube.com/watch?v=7rRYpX5-9RI) or Pygame? or web?
- dashboard for analytics:
    - ball possession
    - goals
    - passes