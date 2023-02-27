import { HopeThemeConfig } from "@hope-ui/solid";

/** The set of default themes given to HopeUI. */
const themeConfig: HopeThemeConfig = {
	components: {
		Anchor: {
			baseStyle: {
				textTransform: "uppercase",
				_hover: {
					textDecoration: "none",
				},
				_focus: {
					// This removes the border when the link is selected
					boxShadow: "none",
				},
			},
		},
	},
};

export default themeConfig;
