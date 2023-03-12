import { notificationService } from "@hope-ui/solid";
import { useNavigate } from "@solidjs/router";
import { AxiosError } from "axios";
import { batch, createSignal } from "solid-js";
import {
	LoginSignUpWrapper,
	LoginSignupInput,
} from "../components/LoginSignUp";
import { displayName, loginUser } from "../hooks/useAuth";

export default function SignUpPage() {
	const [email, setEmail] = createSignal<string>("");
	const [password, setPassword] = createSignal<string>("");

	const [invalidInputs, setInvalidInputs] = createSignal<boolean>(false);
	const [isLoading, setIsLoading] = createSignal<boolean>(false);
	const [errorMsg, setErrorMsg] = createSignal<string>("");
	const [fetchError, setFetchError] = createSignal<AxiosError | undefined>();

	const navigate = useNavigate();

	function handleSubmit() {
		if (email().length === 0 || password().length === 0) {
			setInvalidInputs(true);
			return;
		}

		batch(() => {
			setInvalidInputs(false);
			setIsLoading(true);
		});

		loginUser(email(), password())
			.then(() => {
				notificationService.show({
					title: `Welcome ${displayName()}!`,
					description: "You have logged in successfully 😊",
				});
				navigate("/");
			})
			.catch((err: AxiosError) => {
				if (err.response?.status === 401) {
					setErrorMsg("Incorrect email or password.");
				} else {
					setFetchError(err);
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
				label="Password"
				value={password()}
				onChangeHandler={setPassword}
				invalid={invalidInputs()}
				isPassword
			/>
		</LoginSignUpWrapper>
	);
}
