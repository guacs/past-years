import { Alert, AlertIcon, AlertTitle, AlertDescription } from "@hope-ui/solid";
import { AxiosError, AxiosHeaders } from "axios";
import { Match, Switch } from "solid-js";

// ----- Props Interface/Props -----
interface FetchErrorProps {
	error: AxiosError;
}

// ----- Components -----

/** A common component to be displayed whenever there's an error
 * when trying to fetch from the backend.
 */
export default function FetchError(props: FetchErrorProps) {
	/** Gets the request ID associated with the API call if available.
	 *
	 * @returns The request ID if available. If not, an empty string is
	 * returned.
	 */
	const getRequestId = (): string => {
		const headers = props.error.response?.headers;
		if (!(headers instanceof AxiosHeaders)) return "";

		const requestId = headers.get("x-request-id");
		return requestId ? (requestId as string) : "";
	};

	return (
		<Switch fallback={<h1>Something went wrong...</h1>}>
			<Match when={props.error.message.toLowerCase() === "network error"}>
				<h1>Check your internet connection</h1>
			</Match>
			<Match when={props.error.response !== undefined}>
				<Alert
					status="danger"
					variant="subtle"
					flexDirection="column"
					justifyContent="center"
					textAlign="center"
					height="200px"
				>
					<AlertIcon boxSize="40px" mr="0" />
					<AlertTitle mt="$4" mb="$1" fontSize="$lg">
						Something went wrong!
					</AlertTitle>

					<AlertDescription maxWidth="$sm">
						Please try again, and if this keeps on repeating, please raise a
						support ticket and provide the following ID: {getRequestId()}
					</AlertDescription>
				</Alert>
			</Match>
		</Switch>
	);
}
