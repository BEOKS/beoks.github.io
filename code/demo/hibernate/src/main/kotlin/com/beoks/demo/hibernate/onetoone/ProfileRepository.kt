package com.beoks.demo.hibernate.onetoone

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import java.util.Optional

@Repository
interface ProfileRepository : JpaRepository<Profile, Long> {
    fun findByUserId(userId: Long): Profile?


    fun findByBio(bio: String): Optional<Profile>
}
