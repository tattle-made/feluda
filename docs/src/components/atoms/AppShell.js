import React, { useState } from "react";
import { Grommet, ResponsiveContext, Box, Text } from "grommet";
import TattleTheme from "./Theme";
import SEO from "./SEO";
// import NarrowSection from "./layout/narrow-section"
// import NarrowContentWrapper from "./layout/narrow-content-wrapper"
// import { X } from "react-feather"
import { PlainLink } from "./TattleLinks";
import { useLocation } from "@reach/router";

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
      <Box fill direction={"column"}>
        <SEO title={`Tattle Search Documentation`} />

        <Box height={{ min: "90vh" }} flex={"grow"}>
          {children}
        </Box>
      </Box>
    </Grommet>
  );
};

export default AppShell;
