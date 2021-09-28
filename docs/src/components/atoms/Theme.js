import { css } from "styled-components";

const TattleTheme = {
  global: {
    font: {
      family: "Bitter",
    },
    colors: {
      background: "#ffffff",
      brand: "#E76D67",
      "accent-1": "#514E80",
      "accent-2": "#7F7AB0",
      "accent-3": "#252653",
      "neutral-1": "#E68BBA",
      "neutral-2": "#856993",
      "neutral-3": "#EDC9C4",
      "neutral-4": "#70234B",
      "text-dark": "#edc9c4",
      "text-light": "#fcbfa4",
      "visuals-1": "#ffebcb",
      "visuals-2": "#fcbfa4",
      "visuals-3": "#f4c6d7",
      "visuals-4": "#f39695",
      "visuals-5": "#e99469",
      "visuals-6": "#f3a444",
      "visuals-7": "#e56d67",
      "visuals-8": "#815089",
      "visuals-9": "#4d5182",
      "visuals-10": "#020637",
      text: {
        dark: "#edc9c4",
        light: "#514e80",
      },
    },
    focus: {
      border: {
        color: "accent-1",
      },
    },
  },
  carousel: {
    animation: {
      duration: 0,
    },
  },
  heading: {
    font: {
      family: "Bitter",
    },
    responsive: true,
    responsiveBreakpoint: 400,
    color: {
      dark: "#edc9c4",
      light: "#514e80",
    },
  },
  paragraph: {
    font: {
      family: "Bitter",
    },
  },
  button: {
    border: { radius: "0.2em" },
    default: {
      border: { radius: "small" },
      color: "text",
      padding: {
        horizontal: "small",
        vertical: "xsmall",
      },
      font: {
        family: "Raleway",

        extend: `letter-spacing: 0.2em`,
      },
    },
    primary: {
      background: { color: "brand" },
      extend: `font-size: 1.6em;`,
    },
    secondary: {
      border: { color: "brand", width: "4px", radius: "small" },
      color: "text",
      padding: {
        horizontal: "8px",
        vertical: "4px",
      },
    },
  },
  text: {
    font: {
      family: "Raleway",
    },
    xsmall: {
      size: "11.719px",
      height: "14px",
      maxWidth: "288px",
      weight: 900,
    },
    small: {
      size: "18.75px",
      height: "24px",
      maxWidth: "336px",
    },
    medium: {
      size: "30px",
      height: "40px",
      maxWidth: "432px",
    },
    large: {
      size: "48px",
      height: "54px",
      maxWidth: "528px",
    },
    xlarge: {
      size: "76.8px",
      height: "82px",
      maxWidth: "624px",
    },
    xxlarge: {
      size: "122.88px",
      height: "140px",
      maxWidth: "816px",
    },
    caption: {
      size: "40px",
    },
    primary_navigation: {
      size: "18px",
      family: "Raleway",
    },
  },
  table: {
    body: {
      border: "all",
      pad: { vertical: "none" },
    },
    header: {
      border: "all",
      background: {
        color: "light-2",
      },
    },
  },
  radioButton: {
    font: {
      weight: 400,
    },
    size: "1em",
    container: {
      extend: css`
        font-size: 16px;
        font-family: Raleway;
      `,
    },
  },
};

export default TattleTheme;
