package com.beoks.demo.hibernate.onetoone

import jakarta.persistence.EntityManager
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest
import org.springframework.test.context.ActiveProfiles
import org.assertj.core.api.Assertions.assertThat

@DataJpaTest
@ActiveProfiles("test")
class UserProfileRepositoryTest {

    @Autowired
    private lateinit var entityManager: EntityManager

    @Autowired
    private lateinit var userRepository: UserRepository

    @Autowired
    private lateinit var profileRepository: ProfileRepository

    private lateinit var user1: User
    private lateinit var user2: User
    private lateinit var user3: User
    private lateinit var profile1: Profile
    private lateinit var profile2: Profile
    private lateinit var profile3: Profile

    @BeforeEach
    fun setUp() {
        // 사용자 데이터 초기화
        user1 = User(username = "user1", email = "user1@example.com")
        user2 = User(username = "user2", email = "user2@example.com")
        user3 = User(username = "user3", email = "user3@example.com")

        // 프로필 데이터 초기화
        profile1 = Profile(bio = "첫 번째 사용자의 프로필", avatarUrl = "http://example.com/avatar1.jpg", user = user1)
        profile2 = Profile(bio = "두 번째 사용자의 프로필", avatarUrl = "http://example.com/avatar2.jpg", user = user2)
        profile3 = Profile(bio = "세 번째 사용자의 프로필", avatarUrl = "http://example.com/avatar3.jpg", user = user3)

        // EntityManager를 사용하여 데이터 직접 삽입
        entityManager.persist(user1)
        entityManager.persist(user2)
        entityManager.persist(user3)
        entityManager.persist(profile1)
        entityManager.persist(profile2)
        entityManager.persist(profile3)
        entityManager.flush()
        entityManager.clear()
    }

    @Test
    fun `사용자와 프로필을 저장하고 조회한다`() {
        // when
        val foundUser1 = userRepository.findByUsername("user1")
        val foundProfile1 = profileRepository.findByBio("두 번째 사용자의 프로필").get()

        // then
        assertThat(foundUser1).isNotNull
        assertThat(foundUser1?.username).isEqualTo("user1")
        assertThat(foundProfile1).isNotNull
        assertThat(foundProfile1?.bio).isEqualTo("두 번째 사용자의 프로필")
    }

    @Test
    fun `여러 사용자와 프로필을 저장하고 전체 조회한다`() {
        // when
        val allUsers = userRepository.findAll()
        val allProfiles = profileRepository.findAll()

        // then
        assertThat(allUsers).hasSize(3)
        assertThat(allProfiles).hasSize(3)
        assertThat(allUsers.map { it.username }).containsExactlyInAnyOrder("user1", "user2", "user3")
        assertThat(allProfiles.map { it.bio }).containsExactlyInAnyOrder(
            "첫 번째 사용자의 프로필",
            "두 번째 사용자의 프로필",
            "세 번째 사용자의 프로필"
        )
    }
} 
