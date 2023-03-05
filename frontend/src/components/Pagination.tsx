import { Button, ButtonGroup, Center } from "@hope-ui/solid";
import { For, Index, createSignal } from "solid-js";
import { range } from "../utils";

interface PaginationProps {
	/** The total number of pages to display. */
	numOfPages: number;

	/** The number of page buttons to show. */
	numOfButtons: number;

	/** The starting page number. This is for cases when the user goes
	 * to the page directly from by entering the URL.
	 */
	startingPage: number;

	/** The function to call when a new page is clicked. */
	onPageClick: (pageNum: number) => void;
}

// ---- Styles -----
const buttonFocusStyle = { boxShadow: "none" };

// ----- Components ----

/** Handles pagination of any list of items. */
export default function Pagination(props: PaginationProps) {
	const [currPageNum, setCurrPageNum] = createSignal<number>(
		props.startingPage,
	);

	const [startPageNum, setStartPageNum] = createSignal<number>(
		props.startingPage,
	);

	function handleNewPageClick(newPageNum: number) {
		if (newPageNum > startPageNum() + props.numOfButtons) {
			let startPage;

			/** If the selected page is the last page, then we want
			 *  to make sure that the previous pages are also displayed.
			 *  Also we want to ensure that the previous pages don't go
			 *  below 0 in the case where the number of pages are less
			 *  than the pages buttons to show.
			 */
			if (newPageNum === props.numOfPages - 1) {
				startPage = Math.max(0, newPageNum - props.numOfButtons);
			} else {
				startPage = newPageNum;
			}
			setStartPageNum(startPage);
		} else if (newPageNum < startPageNum()) {
			const startPage = Math.max(newPageNum - props.numOfButtons, 0);
			setStartPageNum(startPage);
		}

		setCurrPageNum(newPageNum);
		props.onPageClick(newPageNum);
	}

	function goToPrevPage() {
		handleNewPageClick(currPageNum() - 1);
	}

	function goToNextPage() {
		handleNewPageClick(currPageNum() + 1);
	}

	function getButtonsRange() {
		const stop = Math.min(
			startPageNum() + props.numOfButtons + 1,
			props.numOfPages,
		);
		const start = startPageNum();
		return range(stop, start);
	}

	return (
		<Center padding="$8">
			<Button
				borderRadius="$full"
				margin="$2"
				variant="ghost"
				onClick={() => handleNewPageClick(0)}
				disabled={currPageNum() === 0}
				_focus={buttonFocusStyle}
			>
				{"<<"}
			</Button>
			<Button
				borderRadius="$full"
				margin="$2"
				variant="ghost"
				onClick={goToPrevPage}
				disabled={currPageNum() === 0}
				_focus={buttonFocusStyle}
			>
				{"<"}
			</Button>
			<Index each={getButtonsRange()}>
				{(pageNum) => (
					<Button
						onClick={() => handleNewPageClick(pageNum())}
						variant={currPageNum() === pageNum() ? "subtle" : "ghost"}
						borderRadius="$full"
						margin="$2"
						_focus={buttonFocusStyle}
					>
						{pageNum() + 1}
					</Button>
				)}
			</Index>
			<Button
				borderRadius="$full"
				margin="$2"
				variant="ghost"
				onClick={goToNextPage}
				disabled={currPageNum() === props.numOfPages - 1}
				_focus={buttonFocusStyle}
			>
				{">"}
			</Button>
			<Button
				borderRadius="$full"
				margin="$2"
				variant="ghost"
				onClick={() => handleNewPageClick(props.numOfPages - 1)}
				disabled={currPageNum() === props.numOfPages - 1}
				_focus={buttonFocusStyle}
			>
				{">>"}
			</Button>
		</Center>
	);
}
