"""unittest module, create coroutine session"""
import sys
from unittest import TestCase, mock, main

sys.path.insert(0, "src")
from GeventLibrary.exceptions import (
    AliasAlreadyCreated,
    NoBundleCreated,
    BundleHasNoCoroutines,
)
from GeventLibrary.keywords.gevent_keywords import GeventKeywords
from GeventLibrary.gevent_library import GeventLibrary 


class TestInstanceCreation(TestCase):
    """This suite tests the creation of new gevent instances"""

    def test_instantiate_keywords_class(self):
        """when a new keyword instance is created,
        it should have no bundle of coroutines"""
        gevent_library_instance = GeventKeywords()
        self.assertEqual(0, len(gevent_library_instance))

    def test_instantiate_keywords_class_patch_threads(self):
        """when a new keyword instance is created,
        it should have no bundle of coroutines"""
        gevent_library_instance = GeventLibrary(patch_threads=True)
        print(gevent_library_instance)

    def test_create_empty_bundle_with_alias(self):
        """When we add a new bundle of coroutines, length should be increased to 1,
        this instance should not contain any coroutines yet"""
        gevent_library_instance = GeventKeywords()
        gevent_library_instance.create_gevent_bundle("my_alias")
        coros = gevent_library_instance["my_alias"]

        self.assertEqual(1, len(gevent_library_instance))
        self.assertEqual(0, len(coros))

    def test_create_empty_bundle_without_alias(self):
        """When we add a new bundle of coroutines, length should be increased to 1,
        without alias, the latest created session should be taken."""
        gevent_library_instance = GeventKeywords()
        gevent_library_instance.create_gevent_bundle()
        coros = gevent_library_instance[None]

        self.assertEqual(1, len(gevent_library_instance))
        self.assertEqual(0, len(coros))

    def test_create_bundle_get_last_created_bundle(self):
        """When we add a new bundle of coroutines, length should be increased to 1,
        without alias, the latest created session should be taken."""
        gevent_library_instance = GeventKeywords()
        gevent_library_instance.create_gevent_bundle()
        gevent_library_instance.add_coroutine("Name1")
        gevent_library_instance.add_coroutine("Name2")
        gevent_library_instance.create_gevent_bundle()
        gevent_library_instance.add_coroutine("Name2")
        coros = gevent_library_instance[None]

        self.assertEqual(2, len(gevent_library_instance))
        # Both coroutines were attached to the first bundle,
        # the second bundle should contain a single coroutine
        self.assertEqual(1, len(coros))

    def test_create_bundle_that_already_exists(self):
        """When we create a new bundle with a name that already exists,
        we expect an 'AliasAlreadyCreated' error raise"""
        with self.assertRaises(AliasAlreadyCreated) as exp:
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
        self.assertEqual(
            str(exp.exception), "An alias with name my_alias has already been created."
        )

    def test_add_coroutine_before_session(self):
        """When we create a new bundle with a name that already exists,
        we expect an 'AliasAlreadyCreated' error raise"""
        with self.assertRaises(NoBundleCreated) as exp:
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.add_coroutine("Name")
        self.assertEqual(
            str(exp.exception),
            "Please create a bundle with `Create Gevent Bundle` keyword",
        )

    def test_run_empty_coroutine_bundle(self):
        """When we run a bundle of coroutines,
        we need to make sure there are coroutines to run,
        in case there aren't, a 'SessionHasNoCoroutines' exception will be raised."""
        with self.assertRaises(BundleHasNoCoroutines) as exp:
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            gevent_library_instance.run_coroutines("my_alias")
        self.assertEqual(
            str(exp.exception),
            "The given bundle has no coroutines, please use `Add Coroutine` keyword",
        )

    def test_bundle_is_empty_after_execution(self):
        """After the bundle is executed, the coroutines should be deleted."""
        with mock.patch(
            "robot.libraries.BuiltIn.BuiltIn.run_keyword", returned_Value=1
        ), mock.patch(
            "robot.running.context.ExecutionContexts.current",
            returned_Value="not null...",
        ):
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            gevent_library_instance.add_coroutine("Log", "Hello World1")
            gevent_library_instance.add_coroutine("Log", "Hello World2")

            coros = gevent_library_instance["my_alias"]
            self.assertEqual(2, len(coros))
            gevent_library_instance.run_coroutines()
            self.assertEqual(0, len(coros))

    def test_using_gevent_pool_positive_number(self):
        """When using a positive number for poolsize"""
        with mock.patch(
            "robot.libraries.BuiltIn.BuiltIn.run_keyword", returned_Value=1
        ), mock.patch(
            "robot.running.context.ExecutionContexts.current",
            returned_Value="not null...",
        ):
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            gevent_library_instance.add_coroutine("Log", "Hello World1")
            gevent_library_instance.add_coroutine("Log", "Hello World2")

            coros = gevent_library_instance["my_alias"]
            self.assertEqual(2, len(coros))
            gevent_library_instance.run_coroutines(gevent_pool_size=3)
            self.assertEqual(0, len(coros))

    def test_using_gevent_pool_zero(self):
        """When using a positive number for poolsize"""
        with mock.patch(
            "robot.libraries.BuiltIn.BuiltIn.run_keyword", returned_Value=1
        ), mock.patch(
            "robot.running.context.ExecutionContexts.current",
            returned_Value="not null...",
        ):
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            gevent_library_instance.add_coroutine("Log", "Hello World1")
            gevent_library_instance.add_coroutine("Log", "Hello World2")

            coros = gevent_library_instance["my_alias"]
            self.assertEqual(2, len(coros))
            gevent_library_instance.run_coroutines(gevent_pool_size=0)
            self.assertEqual(0, len(coros))

    def test_using_gevent_pool_negative_number(self):
        """When using a negative number for poolsize"""
        with mock.patch(
            "robot.libraries.BuiltIn.BuiltIn.run_keyword", returned_Value=1
        ), mock.patch(
            "robot.running.context.ExecutionContexts.current",
            returned_Value="not null...",
        ), self.assertRaises(
            ValueError
        ) as exp:
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            gevent_library_instance.add_coroutine("Log", "Hello World1")
            gevent_library_instance.add_coroutine("Log", "Hello World2")

            coros = gevent_library_instance["my_alias"]
            self.assertEqual(2, len(coros))
            gevent_library_instance.run_coroutines(gevent_pool_size=-3)
            self.assertEqual(0, len(coros))
        self.assertEqual(
            str(exp.exception),
            "'gevent_pool_size' must be a non negative value, got -3",
        )

    def test_order_of_returned_values(self):
        """After the bundle is executed, the coroutines should be deleted."""
        side_effect = [1, 2, "string", {"set"}]
        with mock.patch(
            "robot.libraries.BuiltIn.BuiltIn.run_keyword", side_effect=side_effect
        ), mock.patch(
            "robot.running.context.ExecutionContexts.current",
            returned_Value="not null...",
        ):
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            for _ in side_effect:
                gevent_library_instance.add_coroutine("Convert To Integer", "1")

            values = gevent_library_instance.run_coroutines()
            self.assertListEqual(side_effect, values)

    def test_bundle_does_not_exist(self):
        """After the bundle is executed, the coroutines should be deleted."""
        with self.assertRaises(LookupError) as exp:
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias1")
            gevent_library_instance.create_gevent_bundle(alias="my_alias2")
            gevent_library_instance.create_gevent_bundle(alias="my_alias3")
            gevent_library_instance.add_coroutine(
                "Convert To Integer", "1", alias="my_alias4"
            )
        self.assertEqual(
            str(exp.exception),
            "Bundle with alias my_alias4 was not found",
        )

    def test_keyword_raise_exception(self):
        """After the bundle is executed, the coroutines should be deleted."""
        with mock.patch(
            "robot.libraries.BuiltIn.BuiltIn.run_keyword",
            side_effect=ValueError("some value error..."),
        ), mock.patch(
            "robot.running.context.ExecutionContexts.current",
            returned_Value="not null...",
        ):
            gevent_library_instance = GeventKeywords()
            gevent_library_instance.create_gevent_bundle(alias="my_alias")
            gevent_library_instance.add_coroutine("Convert To Integer", "1")
            with self.assertRaises(ValueError) as exp:
                gevent_library_instance.run_coroutines()
            self.assertEqual(
                str(exp.exception),
                "some value error...",
            )

    def test_remove_one_bundle(self):
        gevent_library_instance = GeventKeywords()
        gevent_library_instance.create_gevent_bundle(alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World1", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World2", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World3", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World4", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World5", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World6", alias="my_alias1")
        gevent_library_instance.create_gevent_bundle(alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World1", alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World2", alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World3", alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World4", alias="my_alias2")
        self.assertEqual(2, len(gevent_library_instance))
        gevent_library_instance.clear_bundle(alias="my_alias1")
        self.assertEqual(1, len(gevent_library_instance))
        coros = gevent_library_instance["my_alias2"]
        self.assertEqual(4, len(coros))
        with self.assertRaises(LookupError) as exp:
            coros = gevent_library_instance["my_alias1"]
        self.assertEqual(
            str(exp.exception),
            "Bundle with alias my_alias1 was not found",
        )

    def test_remove_all_bundles(self):
        gevent_library_instance = GeventKeywords()
        gevent_library_instance.create_gevent_bundle(alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World1", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World2", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World3", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World4", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World5", alias="my_alias1")
        gevent_library_instance.add_coroutine("Log", "Hello World6", alias="my_alias1")
        gevent_library_instance.create_gevent_bundle(alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World1", alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World2", alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World3", alias="my_alias2")
        gevent_library_instance.add_coroutine("Log", "Hello World4", alias="my_alias2")
        self.assertEqual(2, len(gevent_library_instance))
        gevent_library_instance.clear_all_bundles()

        self.assertEqual(0, len(gevent_library_instance))

    def test_remove_a_bundle_that_doesnt_exist(self):
        gevent_library_instance = GeventKeywords()
        with self.assertRaises(LookupError) as exp:
            gevent_library_instance.clear_bundle(alias="my_alias1")
        self.assertEqual(
            str(exp.exception),
            "Bundle with alias my_alias1 was not found",
        )

if __name__ == "__main__":
    main()
