import {
	Button,
	FormControl,
	FormLabel,
	HStack,
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
	Stack,
	VStack,
} from "@hope-ui/solid";
import { Params, useSearchParams } from "@solidjs/router";
import {
	Accessor,
	For,
	Setter,
	createResource,
	createSignal,
	onMount,
} from "solid-js";
import { fetchQuestionsMetadata } from "../api";
import { QuestionsMetadata } from "../types";
import { title } from "../utils";

// ----- Props Interfaces/Types -----
interface FilterProps {
	onSearch: (filter: string) => void;
}

interface SelectChoicesProps<T> {
	choices: T;
	placeholder: string;
	selectedValues: Accessor<T>;
	handleOnChange: Setter<T>;
}

// ----- Components -----

/** The filter component. */
export default function Filter(props: FilterProps) {
	const [query, setQuery] = createSignal<string>("");
	const [exams, setExams] = createSignal<string[]>([]);
	const [subjects, setSubjects] = createSignal<string[]>([]);
	const [years, setYears] = createSignal<string[]>([]);

	const [choices] = createResource(fetchQuestionsMetadata, {
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

		return queryParams.toString();
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
		<VStack m="$10" alignItems="left">
			<form onSubmit={search}>
				<FormControl marginBottom="$3">
					<Input
						id="query"
						value={query()}
						onInput={(e) => setQuery(e.currentTarget.value)}
					/>
				</FormControl>
				<Stack direction={{ "@initial": "column", "@md": "row" }} spacing={5}>
					<FormControl>
						<FormLabel fontSize="lg">Exams</FormLabel>
						<SelectChoices
							choices={choices().exams}
							selectedValues={exams}
							handleOnChange={setExams}
							placeholder="Select an exam"
						/>
					</FormControl>
					<FormControl>
						<FormLabel fontSize="lg">Subjects</FormLabel>
						<SelectChoices
							choices={choices().subjects}
							selectedValues={subjects}
							handleOnChange={setSubjects}
							placeholder="Select a subject"
						/>
					</FormControl>
					<FormControl>
						<FormLabel fontSize="lg">Years</FormLabel>
						<SelectChoices
							choices={choices().years}
							selectedValues={years}
							handleOnChange={setYears}
							placeholder="Select a year"
						/>
					</FormControl>
				</Stack>
				<HStack>
					<Button type="submit" margin="$5" variant="subtle">
						Search
					</Button>
				</HStack>
			</form>
		</VStack>
	);
}

// TODO: Figure out how to style the selected values.
function SelectChoices(props: SelectChoicesProps<string[] | number[]>) {
	return (
		<Select
			multiple
			value={props.selectedValues()}
			onChange={props.handleOnChange}
		>
			<SelectTrigger>
				<SelectPlaceholder>{props.placeholder}</SelectPlaceholder>
				<SelectValue />
				<SelectIcon rotateOnOpen={true} />
			</SelectTrigger>
			<SelectContent>
				<SelectListbox>
					<For each={props.choices}>
						{(e) => (
							<SelectOption value={e}>
								<SelectOptionText>{e}</SelectOptionText>
								<SelectOptionIndicator />
							</SelectOption>
						)}
					</For>
				</SelectListbox>
			</SelectContent>
		</Select>
	);
}
