import { batch, createSignal } from "solid-js";
import { User } from "../types";
import { fetchNewAccessToken, login, logout, signUp } from "../api";

function useAuth() {
	const [user, setUser] = createSignal<User | undefined>();
	const [accessToken, setAccessToken] = createSignal<string>("");

	/** Returns whether the user is logged in or not. */
	function isLoggedIn(): boolean {
		return user() !== undefined;
	}

	/** Returns the display name of the user, if the user is logged in. */
	function displayName() {
		const _user = user();
		console.log(_user);
		if (_user === undefined) {
			console.log("undefined");
			return "";
		}
		return _user.displayName;
	}

	/** Signs up a new user. */
	async function signUpUser(
		email: string,
		displayName: string,
		password: string,
	) {
		await signUp(email, displayName, password);
	}

	/** Logs in the user with the given credentials. */
	async function loginUser(email: string, password: string) {
		const response = await login(email, password);
		setUser(response.user);
		// TODO: Figure out if there's a safer way to store this.
		localStorage.setItem("refresh-token", response.refreshToken);
	}

	/** Returns the access token if available. If that's not available,
	 * then a new access token is created by calling the endpoint with
	 * the refresh token.
	 */
	async function getAccessToken() {
		if (accessToken().length !== 0) {
			return accessToken;
		}
		return await refreshAccessToken();
	}

	/** Gets a new access token with the refresh token if possible. */
	async function refreshAccessToken() {
		const refreshToken = localStorage.getItem("refresh-token");
		if (!refreshToken) {
			return "";
		}

		return await fetchNewAccessToken(refreshToken)
			.then((newAccessToken) => {
				setAccessToken(newAccessToken);
				return newAccessToken;
			})
			.catch(() => {
				return "";
			});
	}

	/** Logs out the current user. */
	async function logoutUser() {
		const _user = user();
		if (!_user) return;
		await logout(_user.userId);

		batch(() => {
			setUser(undefined);
			setAccessToken("");
		});
		localStorage.removeItem("refresh-token");
	}

	return {
		user,
		isLoggedIn,
		displayName,
		loginUser,
		logoutUser,
		signUpUser,
		getAccessToken,
	};
}

const {
	user,
	isLoggedIn,
	displayName,
	loginUser,
	logoutUser,
	getAccessToken,
	signUpUser,
} = useAuth();

export {
	user,
	isLoggedIn,
	displayName,
	loginUser,
	logoutUser,
	getAccessToken,
	signUpUser,
};
