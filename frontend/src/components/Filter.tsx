import {
	Button,
	Flex,
	FormControl,
	FormLabel,
	Input,
	Select,
	SelectContent,
	SelectIcon,
	SelectListbox,
	SelectOption,
	SelectOptionIndicator,
	SelectOptionText,
	SelectPlaceholder,
	SelectTrigger,
	SelectValue,
	useColorMode,
} from "@hope-ui/solid";
import { Params, useSearchParams } from "@solidjs/router";
import { For, Setter, createResource, createSignal, onMount } from "solid-js";
import { fetchQuestionsMetadata } from "../api";
import { title } from "../utils";

// ----- Props Interfaces/Types -----
interface FilterProps {
	/** The function to call with a new set of filters. */
	onSearch: (filter: string) => void;
}

interface FilterChoicesProps<T extends string | number> {
	/** The label to give to the select choice. */
	label: string;
	/** The available options in the dropdown. */
	choices: T[];
	/** The selected values from the dropdown. */
	selectedValues: T[];
	/** Handling adding/removing selections from the dropdown. */
	handleOnChange: Setter<T[]>;
}

// ----- Components -----

/** The filter component. */
export default function Filter(props: FilterProps) {
	const [query, setQuery] = createSignal<string>("");
	const [exams, setExams] = createSignal<string[]>([]);
	const [subjects, setSubjects] = createSignal<string[]>([]);
	const [years, setYears] = createSignal<string[]>([]);

	const { colorMode } = useColorMode();
	/** The available options in the filters. */
	const [filterOptions] = createResource(fetchQuestionsMetadata, {
		initialValue: {
			exams: [],
			subjects: [],
			years: [],
		},
	});

	const [searchParams, setSearchParams] = useSearchParams();

	onMount(() => {
		// This is to ensure that the search is done based on the existing query
		// parameters if there are any query parameters in the URL if there
		// for the cases where the user directly comes from a link.
		const examValues: string[] = getFiltersFromUrl("exams").map((e) =>
			e.toUpperCase(),
		);
		const subjectValues: string[] = getFiltersFromUrl("subjects").map((s) =>
			title(s),
		);
		const yearValues: string[] = getFiltersFromUrl("years");

		// Implies no query given via the query string so default
		// to the default query of the latest CSE exam.
		if (!(examValues.length || subjectValues.length || yearValues.length)) {
			examValues.push("CSE");
			yearValues.push("2022");
		}

		setExams(examValues);
		setSubjects(subjectValues);
		setYears(yearValues);

		search();
	});

	/** Helper to get the values of the search parameters. */
	function getFiltersFromUrl(param: string): string[] {
		const values = searchParams[param];
		if (values === undefined) return [];
		return values.split(",");
	}

	/** Creates the query string from the selected filters. */
	function createQueryString(): string {
		const queryParams = new URLSearchParams();

		exams().forEach((e) => queryParams.append("exams", e));
		subjects().forEach((s) => queryParams.append("subjects", s));
		years().forEach((y) => queryParams.append("years", y));
		if (query().length !== 0) {
			queryParams.set("q", query());
		}

		return queryParams.toString().toLowerCase();
	}

	/** Sets the new search parameters with the values in the filters. */
	function setNewSearchParams(): void {
		const newSearchParams: Params = {
			q: "",
			subjects: "",
			exams: "",
			years: "",
		};
		if (exams().length !== 0) {
			newSearchParams.exams = exams().join(",");
		}
		if (subjects().length !== 0) {
			newSearchParams.subjects = subjects().join(",");
		}
		if (years().length !== 0) {
			newSearchParams.years = years().join(",");
		}
		if (query().length !== 0) {
			newSearchParams.q = query();
		}

		setSearchParams(newSearchParams);
	}

	/** Searches for the questions provided the given filters. */
	function search(event?: Event) {
		if (event !== undefined) {
			event.preventDefault();
		}

		setNewSearchParams();

		const queryString = createQueryString();
		props.onSearch(queryString);
	}

	return (
		<form onSubmit={search}>
			<Flex m="$10" flexDirection="column">
				<Input
					id="query"
					value={query()}
					onInput={(e) => setQuery(e.currentTarget.value)}
					placeholder="Search"
					type="search"
				/>
				<Flex
					flexDirection={{ "@initial": "column", "@md": "row" }}
					justifyContent="space-evenly"
				>
					<FilterChoices
						label={"Exams"}
						choices={filterOptions().exams}
						selectedValues={exams()}
						handleOnChange={setExams}
					/>
					<FilterChoices
						label={"Subjects"}
						choices={filterOptions().subjects}
						selectedValues={subjects()}
						handleOnChange={setSubjects}
					/>
					<FilterChoices
						label={"Years"}
						choices={filterOptions().years}
						selectedValues={years()}
						handleOnChange={setYears}
					/>
				</Flex>
				<Button
					onClick={search}
					type="submit"
					maxW="$24"
					marginLeft="$5"
					marginTop="$5"
					colorScheme="info"
					variant={colorMode() === "light" ? "solid" : "subtle"}
				>
					Search
				</Button>
			</Flex>
		</form>
	);
}

function FilterChoices<T extends string | number>(
	props: FilterChoicesProps<T>,
) {
	return (
		<FormControl m="$5">
			<Flex alignItems="center">
				<FormLabel fontSize="$md" m="$2">
					{props.label}
				</FormLabel>
				<Select
					multiple
					value={props.selectedValues}
					onChange={props.handleOnChange}
				>
					<SelectTrigger>
						<SelectPlaceholder>
							Select {props.label.toLowerCase()}
						</SelectPlaceholder>
						<SelectValue />
						<SelectIcon rotateOnOpen />
						<SelectContent>
							<SelectListbox>
								<For each={props.choices}>
									{(c) => (
										<SelectOption value={c}>
											<SelectOptionText>{c}</SelectOptionText>
											<SelectOptionIndicator />
										</SelectOption>
									)}
								</For>
							</SelectListbox>
						</SelectContent>
					</SelectTrigger>
				</Select>
			</Flex>
		</FormControl>
	);
}
