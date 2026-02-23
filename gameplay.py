class Protocol:
    def __init__(self):
        self.next_states : [int, int|str] = {}
        self.states : [int, State]

    def get_initial_state(self):
        pass


class State:
    def __init__(self, protocol: Protocol):
       self.protocol = protocol
       self.id = None

    def correct_answer(self):
        pass

    def sample_wrong_answers(self, n=3):
        pass

    def get_next_state(self):
        return random.choice(self.protocol.next_states[self.id])


class Gameplay:
    def __init__(self, app):
        self.app = app
        self.current_protocol = self.app.get_player_protocol()
        self.current_state = self.current_protocol.get_initial_state()

    def loop(self):
        while True:
            # Some states are final. That means there are no possible answers, but rather a description of the final state. The app should show the score and the loop ends.
            if self.current_state.type == "final":
                self.app.show(state=self.current_state.description, answers=None, show_scores=True)
                return

            # Otherwise, fetch the wrong and correct answers. Shuffle them. Show them to the user. Get his answers and offer feedback in the app.
            wrong_answers = self.current_state.sample_wrong_answers()
            correct_answer = self.current_state.get_correct_answer()
            answers = random.shuffle([*wrong_answers, correct_answer])
            self.app.show(state=self.current_state.description, answers=answers):
            choice = self.app.get_player_choice()
            if self.is_correct(choice):
                self.app.increase_score()
                self.app.show_feedback(self.state.feedback, correct=True)
            else:
                self.app.show_feedback(self.state.feedback, correct=False)

            # Handle changing the state. It is possible the next state is another protocol. In that case change the current protocol and set the current state to be it's initial state. Otherwise get the next state from the current protocol.
            next_state = self.current_state.get_next_state()
            if type(next_state) is str:
                self.current_protocol = protocls[next_state]
                self.current_state = self.current_protocol.get_initial_state()
            else:
                self.current_state = self.current_protocol.states[next_state]



