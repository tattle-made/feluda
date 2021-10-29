import React from "react";
import { Grommet, ResponsiveContext, Box, Text, Heading } from "grommet";
import TattleTheme from "./Theme";
import SEO from "./SEO";
// import NarrowSection from "./layout/narrow-section"
// import NarrowContentWrapper from "./layout/narrow-content-wrapper"
// import { X } from "react-feather"
import { PlainLink } from "./TattleLinks";
import TattleLogo from "./TattleLogo";
import { useLocation } from "@reach/router";

const Menu = () => (
  <Box width={"medium"} overflow={"hidden"} margin={{ top: "medium" }}>
    <PlainLink to={"/"}>
      <Heading level={4} margin={"none"}>
        Overview
      </Heading>
    </PlainLink>
    <Box pad={"small"}>
      <PlainLink to="/architecture">
        <Text size={"small"}>Architecture</Text>
      </PlainLink>
      <PlainLink to="/development">
        <Text size={"small"}>Development</Text>
      </PlainLink>
      <PlainLink to="/burns">
        <Text size={"small"}>Burns</Text>
      </PlainLink>
      <PlainLink to="/todo">
        <Text size={"small"}>TODO</Text>
      </PlainLink>
      <PlainLink to="/testing">
        <Text size={"small"}>Testing</Text>
      </PlainLink>
      <PlainLink to="/rough">
        <Text size={"small"}>Rough</Text>
      </PlainLink>
    </Box>
    <PlainLink to={"/operators/"}>
      <Heading level={4} margin={"none"}>
        Operators
      </Heading>
    </PlainLink>
    <Box pad={"small"}>
      <PlainLink to="/operators/text-extractor">
        <Text size={"small"}>Text Extractor</Text>
      </PlainLink>
      <PlainLink to="/operators/vid-vec-rep-resnet">
        <Text size={"small"}>Vid Vec Rep Resnet</Text>
      </PlainLink>
    </Box>
  </Box>
);

/**
 * @author
 * @function ContentPageLayout
 **/

const AppShell = ({
  children,
  footerItems,
  headerTarget,
  primaryNav,
  expandCenter,
  contentWidth,
  isMDXPage,
}) => {
  const size = React.useContext(ResponsiveContext);
  const location = useLocation();

  return (
    <Grommet theme={TattleTheme} full>
      <SEO title={`Tattle Search Documentation`} />
      <Box
        fill
        direction={"row"}
        height={{ min: "90vh", height: "fit-content" }}
        pad={"small"}
      >
        <Box width={"960px"} height={"fit-content"}>
          <Box>
            <TattleLogo />
          </Box>
          <Box direction={"row"}>
            <Menu />

            <Box width={"100%"}>{children}</Box>
          </Box>
        </Box>
      </Box>
    </Grommet>
  );
};

export default AppShell;
