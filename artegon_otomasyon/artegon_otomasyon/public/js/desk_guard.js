(function () {
	function patch_sidebar_guard() {
		if (!window.frappe || !frappe.ui || !frappe.ui.Sidebar) return;
		if (frappe.ui.Sidebar.__artegon_guard_applied) return;

		const Sidebar = frappe.ui.Sidebar;
		const original_get_workspace_sidebars = Sidebar.prototype.get_workspace_sidebars;
		const original_set_workspace_sidebar = Sidebar.prototype.set_workspace_sidebar;

		Sidebar.prototype.get_workspace_sidebars = function (link_to) {
			// Empty route fragments can crash sidebar setup when section rows have no link target.
			if (link_to === undefined || link_to === null || link_to === "") {
				return this.sidebar_title ? [this.sidebar_title] : [];
			}

			const sidebars = original_get_workspace_sidebars.call(this, link_to) || [];
			return sidebars.filter(Boolean);
		};

		Sidebar.prototype.set_workspace_sidebar = function (router) {
			try {
				return original_set_workspace_sidebar.call(this, router);
			} catch (error) {
				// Fallback to a stable sidebar instead of leaving the desk blank.
				console.warn("ARTEGON sidebar guard fallback", error);
				const fallback_sidebar = this.sidebar_title || "ARTEGON";
				if (fallback_sidebar) {
					this.setup(fallback_sidebar);
				}
			}
		};

		Sidebar.__artegon_guard_applied = true;
	}

	if (window.frappe && typeof frappe.after_ajax === "function") {
		frappe.after_ajax(() => patch_sidebar_guard());
	}

	patch_sidebar_guard();
	window.setTimeout(patch_sidebar_guard, 0);
	window.setTimeout(patch_sidebar_guard, 500);
})();
