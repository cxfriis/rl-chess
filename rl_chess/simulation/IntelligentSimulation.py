from rl_chess.domain.board.ChessBoard import ChessBoard
from rl_chess.service.AgentService import AgentService
from rl_chess.service.DQN import DQN
from rl_chess.service.PieceMovementService import PieceMovementService


class IntelligentSimulation:

    @staticmethod
    def run():
        chess_board = ChessBoard()
        agent_service = AgentService()

        state_size = 64 + 1
        action_size = 64 * 63

        dqn_agent = DQN(state_size, action_size)
        batch_size = 32
        episodes = 1000

        for e in range(episodes):
            chess_board.reset()
            state = agent_service.get_state(chess_board)

            for time in range(500):
                action = dqn_agent.act(state)
                if agent_service.is_action_legal(chess_board, state, action):
                    print(f'Took {time} tries for agent to pick a legal move on episode {e}')
                    next_state, reward, done = agent_service.step(chess_board, action)
                else:
                    next_state = state
                    reward = -1
                    done = False
                dqn_agent.remember(state, action, reward, next_state, done)
                if done:
                    print("episode: {}/{}, score: {}, e: {:.2}"
                          .format(e, episodes, time, dqn_agent.epsilon))
                    break

            if len(dqn_agent.memory) > batch_size:
                dqn_agent.replay(batch_size)
            if e % 10 == 0:
                dqn_agent.save("./intelligent-simulation.h5")
