import React from "react"
// import { primaryNav, footerItems } from "../config/options"
import AppShell from "./atoms/AppShell"
/**
 * @author
 * @function DefaultLayout
 **/

const DefaultLayout = ({ children }) => (
  <AppShell
    headerLabel={"Khoj Docs"}
  >
    {children}
  </AppShell>
)

export default DefaultLayout
