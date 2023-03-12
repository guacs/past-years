import { notificationService } from "@hope-ui/solid";
import { useNavigate } from "@solidjs/router";
import { AxiosError } from "axios";
import { batch, createSignal } from "solid-js";
import {
	LoginSignUpWrapper,
	LoginSignupInput,
} from "../components/LoginSignUp";
import { signUpUser } from "../hooks/useAuth";

export default function SignUpPage() {
	const [email, setEmail] = createSignal<string>("");
	const [displayName, setDisplayName] = createSignal<string>("");
	const [password, setPassword] = createSignal<string>("");

	const [invalidInputs, setInvalidInputs] = createSignal<boolean>(false);
	const [isLoading, setIsLoading] = createSignal<boolean>(false);
	const [errorMsg, setErrorMsg] = createSignal<string>("");

	const navigate = useNavigate();

	function handleSubmit() {
		if (
			email().length === 0 ||
			displayName().length === 0 ||
			password().length === 0
		) {
			setInvalidInputs(true);
			return;
		}

		batch(() => {
			setInvalidInputs(false);
			setIsLoading(true);
		});

		signUpUser(email(), displayName(), password())
			.then(() => {
				notificationService.show({
					title: "Signed up!",
					description:
						"You signed up successfully. You will be redirected to the login page.",
				});
				navigate("/login");
			})
			.catch((err: AxiosError) => {
				const data = err.response?.data;
				if (data && typeof data === "object") {
					if ("title" in data && data.title === "UserAlreadyExists") {
						setErrorMsg("A user with that email already exists.");
					}
				}
			})
			.finally(() => {
				setIsLoading(false);
			});
	}

	return (
		<LoginSignUpWrapper
			handleSubmit={handleSubmit}
			isLoading={isLoading()}
			errorMsg={errorMsg()}
		>
			<LoginSignupInput
				label="Email"
				value={email()}
				onChangeHandler={setEmail}
				invalid={invalidInputs()}
			/>
			<LoginSignupInput
				label="Name"
				value={displayName()}
				onChangeHandler={setDisplayName}
				invalid={invalidInputs()}
			/>
			<LoginSignupInput
				label="Password"
				value={password()}
				onChangeHandler={setPassword}
				invalid={invalidInputs()}
				isPassword
			/>
		</LoginSignUpWrapper>
	);
}
