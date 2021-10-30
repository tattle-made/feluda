import React from "react";
// import { primaryNav, footerItems } from "../config/options"
import AppShell from "./atoms/AppShell";
import { defineCustomElements as deckDeckGoHighlightElement } from "@deckdeckgo/highlight-code/dist/loader";
deckDeckGoHighlightElement();

/**
 * @author
 * @function DefaultLayout
 **/

const DefaultLayout = ({ children }) => (
  <AppShell headerLabel={"Khoj Docs"}>{children}</AppShell>
);

export default DefaultLayout;
