import {
	Anchor,
	Box,
	Button,
	Flex,
	FormControl,
	FormErrorMessage,
	FormLabel,
	Heading,
	Input,
	Text,
	useColorMode,
} from "@hope-ui/solid";
import { ParentProps, Show, children } from "solid-js";
import FetchError from "./FetchError";
import { A } from "@solidjs/router";
import { AxiosError } from "axios";

interface LoginSignupInputProps {
	label: string;
	value: string;
	onChangeHandler: (newValue: string) => void;
	isPassword?: boolean;
	invalid: boolean;
}

interface LoginSignUpWrapperProps extends ParentProps {
	isLogin?: boolean;
	handleSubmit: () => void;
	isLoading: boolean;
	fetchError?: AxiosError;
	errorMsg: string;
}

export function LoginSignUpWrapper(props: LoginSignUpWrapperProps) {
	const c = children(() => props.children);

	const { colorMode } = useColorMode();

	function getDisplayText() {
		return props.isLogin ? "Login" : "Signup";
	}

	function handleFormSubmit(e: Event) {
		e.preventDefault();
		props.handleSubmit();
	}

	return (
		<Flex
			flexDirection="column"
			justifyContent="center"
			alignItems="center"
			marginLeft="$20"
			marginRight="$20"
			css={{
				minH: "calc(100vh - 80px)",
			}}
		>
			<Heading fontSize={{ "@initial": "$4xl", "@md": "$6xl" }}>
				{getDisplayText()}
			</Heading>
			<Box
				p="$10"
				bgColor={colorMode() === "light" ? "$neutral1" : "$neutral2"}
				borderRadius="$2xl"
				maxW="$5xl"
			>
				<form onSubmit={handleFormSubmit}>
					{c()}
					<Show when={props.errorMsg.length !== 0}>
						<Text mt="$4" color="$danger10">
							{props.errorMsg}
						</Text>
					</Show>
					<Button
						type="submit"
						loading={props.isLoading}
						colorScheme="accent"
						m="$4"
					>
						{getDisplayText()}
					</Button>
				</form>
			</Box>
			<Box
				bgColor={colorMode() === "light" ? "$neutral1" : "$neutral2"}
				borderRadius="$2xl"
				marginTop="$5"
				p="$4"
				minW={{ "@initial": "$36", "@md": "$96" }}
			>
				<Show
					when={!props.isLogin}
					fallback={
						<Text>
							Already have an account?{" "}
							<A href="/login">
								<Text color="$accent9" as="span">
									Login!
								</Text>
							</A>
						</Text>
					}
				>
					<Text>
						Don't have an account?{" "}
						<A href="/sign-up">
							<Anchor color="$accent9" as="span">
								Sign up!
							</Anchor>
						</A>
					</Text>
				</Show>
			</Box>
			<Show when={props.fetchError !== undefined}>
				<FetchError error={props.fetchError} />
			</Show>
		</Flex>
	);
}

export function LoginSignupInput(props: LoginSignupInputProps) {
	return (
		<FormControl
			required
			aria-required
			invalid={props.invalid && props.value.length === 0}
			m="$4"
			maxW="$64"
		>
			<FormLabel>{props.label}</FormLabel>
			<Input
				type={props.isPassword ? "password" : "text"}
				value={props.value}
				onChange={(e) => props.onChangeHandler(e.currentTarget.value)}
			/>
			<FormErrorMessage>{props.label} is required.</FormErrorMessage>
		</FormControl>
	);
}
