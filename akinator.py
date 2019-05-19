import requests

# Somebody told me that the link has changed, but I'm not
# really maintaining this anymore, so here is something that
# I think should fix it.

NEW_SESSION_URL = "https://srv2.akinator.com:9157/ws/new_session?constraint=ETAT<>'AV'&partner=1"
ANSWER_URL = "https://srv2.akinator.com:9157/ws/answer?constraint=ETAT<>'AV'"
GET_GUESS_URL = "https://srv2.akinator.com:9157/ws/list?constraint=ETAT<>'AV'"
CHOICE_URL = "https://srv2.akinator.com:9157/ws/choice?constraint=ETAT<>'AV'"
EXCLUSION_URL = "https://srv2.akinator.com:9157/ws/exclusion?constraint=ETAT<>'AV'"
GLB_URL = "https://pastebin.com/gTua3dg2"


def ans_to_strint(ans: str):
    ans = ans.lower()
    if ans == "yes" or ans == "y":
        return "0"
    elif ans == "no" or ans == "n":
        return "1"
    elif ans == "i" or ans == "idk" or ans == "i dont know" or ans == "i don't know":
        return "2"
    elif ans == "probably" or ans == "p":
        return "3"
    elif ans == "probably not" or ans == "pn":
        return "4"
    else:
        return "-1"


game_over = False

akinator_session = requests.get(NEW_SESSION_URL)
akinator_data = akinator_session.json()


try:
    if akinator_data['completion'] == "OK":
        success = True
    else:
        success = False
except:
    success = False
if not success:
    raise Exception('Error')

print("Question " +
      str(int(akinator_data['parameters']['step_information']['step']) + 1) +
      ":\n" +
      akinator_data['parameters']['step_information']['question'] +
      '\n"yes", "no", "idk", "probably", "probably not"')
response = input("> ")

response = ans_to_strint(response)

params = {
    "session": akinator_data['parameters']['identification']['session'],
    "signature": akinator_data['parameters']['identification']['signature'],
    "step": akinator_data['parameters']['step_information']['step'],
    "answer": response
}

session = akinator_data['parameters']['identification']['session']
signature = akinator_data['parameters']['identification']['signature']

akinator_session = requests.get(ANSWER_URL, params=params)
akinator_data = akinator_session.json()

can_guess = False
guessed_wrong_once = False

while not game_over:
    while not can_guess:
        if int(float(akinator_data['parameters']['progression'])) > 90 and not guessed_wrong_once:
            can_guess = True
            break

        guessed_wrong_once = False

        print(akinator_data['parameters']['progression'])
        print("Question " +
              str(int(akinator_data['parameters']['step']) + 1) +
              ":\n" +
              akinator_data['parameters']['question'] +
              '\n"yes", "no", "idk", "probably", "probably not"')
        response = input("> ")
        response = ans_to_strint(response)

        params = {
            "session": session,
            "signature": signature,
            "step": akinator_data['parameters']['step'],
            "answer": response
        }

        akinator_session = requests.get(ANSWER_URL, params=params)
        akinator_data = akinator_session.json()

    params = {
        "session": session,
        "signature": signature,
        "step": akinator_data['parameters']['step']
    }

    guess_session = requests.get(GET_GUESS_URL, params=params)
    guess_data = guess_session.json()

    name = guess_data['parameters']['elements'][0]['element']['name']
    desc = guess_data['parameters']['elements'][0]['element']['description']

    print("Is this your character? [yes/no]\n" +
          name + "\n" +
          desc + "\n")
    answer = input('> ')

    if answer.lower() == "yes" or answer.lower() == "y":
        #  TODO dump to choice_url
        params = {
            "session": session,
            "signature": signature,
            "step": akinator_data['parameters']['step'],
            "element": guess_data['parameters']['elements'][0]['element']['id']
        }
        r = requests.get(CHOICE_URL, params=params)
        print("I guessed right! Thanks for playing with me.")
        game_over = True
        break

    elif answer.lower() == "no" or answer.lower() == "n":
        #  TODO dump to exclusion_url
        params = {
            "session": session,
            "signature": signature,
            "step": akinator_data['parameters']['step'],
            "forward_answer": response
        }
        r = requests.get(EXCLUSION_URL, params=params)
        can_guess = False
        guessed_wrong_once = True

    else:
        pass
