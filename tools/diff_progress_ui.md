*** a/src/lcpi/core/progress_ui.py
--- b/src/lcpi/core/progress_ui.py
@@
     def handle_generation_start(self, data: dict):
-        total = data.get("total_generations", None)
+        total = data.get("total_generations", None)
         pop = data.get("population_size", None)
-        if pop and 'population' in self.tasks:
-            # reset population bar
-            self.progress.reset(self.tasks['population'])
+        if pop and 'population' in self.tasks:
+            # reset population bar and ensure completed==0 with proper description
+            self.progress.update(self.tasks['population'], completed=0,
+                                 description=f"Éval 0/{pop}")
             # set new total if provided
-            self.progress.update(self.tasks['population'], total=pop)
+            self.progress.update(self.tasks['population'], total=pop)
@@
     def handle_individual_end(self, data: dict):
-        idx = data.get("index", 0)
-        if 'population' in self.tasks:
-            self.progress.update(self.tasks['population'], completed=idx)
+        idx = data.get("index", None)
+        # fallback behavior: if index missing or 0, increment current by 1
+        if 'population' in self.tasks:
+            try:
+                total = self.progress.tasks[self.tasks['population']].total
+            except Exception:
+                total = None
+            if not idx or int(idx) <= 0:
+                # read current completed and bump at least by 1
+                cur = int(self.progress.tasks[self.tasks['population']].completed or 0)
+                idx = min((cur + 1), total) if total else (cur + 1)
+            # ensure we don't exceed total
+            if total and int(idx) > total:
+                idx = total
+            self.progress.update(self.tasks['population'], completed=int(idx),
+                                 description=f"Éval {int(idx)}/{total or '?'}")
